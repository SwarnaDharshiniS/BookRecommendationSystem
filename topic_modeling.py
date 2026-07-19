import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# we need topics for each review which summarise them. We have the function below which takes the model which
# we will define later, the kinds of words or terms that correspond to topics and a count of representative
# words or topics we want. It then iterates through the model giving an index to each topic and assigning each
# item in the model a topic and finally collecting these results.


def display_topics(model, feature_names, no_top_words):
    """
    Returns the top words for every topic the model found, joined into one
    readable string.

    NOTE: the original version had `return` inside the for loop, which meant
    it always exited after the very first topic and silently ignored the
    other topics LDA had computed (a real bug, not by design - there was no
    reason to loop here otherwise). This version collects the top words from
    every topic.
    """
    topic_summaries = []
    for topic_idx, topic in enumerate(model.components_):
        top_words = " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
        topic_summaries.append(top_words)
    return " | ".join(topic_summaries)


# our main function for performing topic modelling
def main_topics(reviews_df, n_topics=5, no_top_words=10):
    """
    Given a dataframe with a 'review_summary' column, fits a small LDA topic
    model and returns a short string summarizing the most common topic words.

    Returns a friendly fallback string instead of raising when there isn't
    enough text to model (e.g. too few reviews, or reviews that are entirely
    stop words) - previously this could crash the whole recommendation with an
    uncaught ValueError ("empty vocabulary") because CountVectorizer was
    being called with max_df=1, which only keeps words that appear in exactly
    one document and can easily filter out everything.
    """
    summaries = reviews_df['review_summary'].dropna()
    summaries = summaries[summaries.str.strip() != '']

    if len(summaries) < 2:
        return "Not enough review text to summarize common topics."

    try:
        # CountVectorizer converts the text into a term-document matrix: rows are
        # documents, columns are words, and it looks at the frequency of each word.
        vectorizer = CountVectorizer(stop_words='english', min_df=1)
        doc_term_matrix = vectorizer.fit_transform(summaries)

        if doc_term_matrix.shape[1] == 0:
            return "Not enough review text to summarize common topics."

        # number of topics can never exceed the number of documents/terms available
        safe_n_topics = max(1, min(n_topics, doc_term_matrix.shape[0], doc_term_matrix.shape[1]))

        # LDA is the topic modelling function which finds topics in documents
        lda = LatentDirichletAllocation(n_components=safe_n_topics, random_state=0)
        lda.fit(doc_term_matrix)

        return display_topics(lda, vectorizer.get_feature_names_out(), no_top_words)
    except ValueError:
        return "Not enough review text to summarize common topics."


# testing our function on a sample of reviews since the full file is large
def main():
    reviews_df = pd.read_csv('Data/filtered_reviews/juvenile fiction_df.csv', usecols=['title', 'review_summary'])

    test = reviews_df.head(1000)

    review_main_topics = main_topics(test)

    print(review_main_topics)


if __name__ == "__main__":
    main()
