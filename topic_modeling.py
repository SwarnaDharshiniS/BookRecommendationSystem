import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


# we need topics for each review which summarise them. We have the function below which takes the model which we will define later,
# the kinds of words or terms that correspond to topics and a count of representative words or topics we want. It then iterates through the
# model giving an index to each topic and assigning each item in the model a topic and finally printing these results.

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        return " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])

# our main function for performing topic modelling

def main_topics(reviews_df):
    # CountVectorizer converts the text into a term-document matrix. Rows correspond to documents and columns to words and looks at frequency of words.
    vectorizer = CountVectorizer(max_df=1, min_df=1, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(reviews_df['review_summary'])
    # LDA is the topic modelling function which finds topics in documents - we have specified 5 topics per document
    lda = LatentDirichletAllocation(n_components=5, random_state=0)
    lda.fit(doc_term_matrix)

    # we then use the previous function to display the top 10 words given to each of the 5 topics
    no_top_words = 10
    return display_topics(lda, vectorizer.get_feature_names_out(), no_top_words)


# testing our function on the top 1000 reviews as our file is currently too large to run quickly
def main():
    reviews_df = pd.read_csv('Data/filtered_reviews/juvenile fiction_df.csv', usecols=['title', 'review_summary'])

    test = reviews_df.head(1000)

    review_main_topics = main_topics(test)

    print(review_main_topics)


if __name__ == "__main__":
    main()