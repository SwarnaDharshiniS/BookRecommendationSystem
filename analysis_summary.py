import pandas as pd
from topic_modeling import main_topics
from sentiment_analysis import apply_sentiment_analysis
import os
from fuzzywuzzy import fuzz

'''
This function returns a boolean given a keyword (or similar word) is found in the review text
'''
def has_keywords(text, keywords):
    if isinstance(text, str):
        # Convert text to lowercase
        text = text.lower()
        # Split text into words
        words = text.split()
        threshold = 80
        for keyword in keywords:
            for word in words:
                # Check similarity between each word and keyword
                if fuzz.ratio(keyword.lower(), word) >= threshold:
                    return True
        return False

'''
This function takes a dataframe and keywords and returns books in the dataframe which contain
the given keywords in their reviews
'''
def matched_books(reviews_df, keywords):
    matching_books = []
    seen_titles = set()
    # loops through the reviews dataframe and checks the title is unique
    for _, review in reviews_df.iterrows():
        # assigns a keyword score to each title
        keyword_score = 1 if has_keywords(review['review_summary'], keywords) else 0
        #review['keyword match'] = keyword_score
        if review['title'] not in seen_titles and keyword_score == 1:
            # a dictionary value is created with the given book data from the dataframe
            matching_books.append({
                'title': review['title'],
                'categories': review['categories'],
                'review_summary': review['review_summary'],
                'review_score': review['review_score'],
                'publisher': review['publisher'],
                'keyword match': keyword_score
            })
            seen_titles.add(review['title'])
    return matching_books

def recommend_book(genre, key_term):
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_path, f"Data/filtered_reviews/{genre}_df.csv")
    reviews_df = pd.read_csv(file_path, usecols=['title', 'categories', 'review_summary', 'review_score', 'publisher'])

    keywords = key_term.split()
    #call the matched_books function to find books with given keywords
    if len(matched_books(reviews_df, keywords)) == 0:
        return pd.DataFrame(), []
    else:
        matching_books = pd.DataFrame(matched_books(reviews_df, keywords))
        #apply the sentiment analysis to the current pool of books
        recommended_books = apply_sentiment_analysis(matching_books)
        #calculate a score for the books based on the sentiment anlaysis and the review score from the previous dataframe
        recommended_books['total_score'] = (recommended_books['review_score']+recommended_books['sentiment'])/2
        #sorts books by this calculated score
        recommended_books = recommended_books.sort_values(by=['total_score'], ascending=False)

        #outputs the top 10
        top_10_recommended = recommended_books.head(10)
        review_topics = main_topics(top_10_recommended)
        return top_10_recommended, review_topics

def main():
    # some fillers of the users input: we have genre and given key words to narrow down books
    keywords = ['serious', 'melancholy']
    genre = 'biography autobiography'

    reviews_df = pd.read_csv(f"Data/filtered_reviews/{genre}_df.csv", usecols=['title', 'categories',
                                                                               'review_summary', 'review_score',
                                                                               'publisher'])
    #call the matched_books function to find books with given keywords
    matching_books = matched_books(reviews_df, keywords)
    #apply the sentiment analysis to the current pool of books
    recommended_books = apply_sentiment_analysis(matching_books)
    #calculate a score for the books based on the sentiment anlaysis and the review score from the previous dataframe
    recommended_books['total_score'] = (recommended_books['review_score']+recommended_books['sentiment'])/2
    #sorts books by this calculated score
    recommended_books = recommended_books.sort_values(by=['total_score'], ascending=False)

    #outputs the top 10
    top_10_recommended = recommended_books.head(10)
    review_topics = main_topics(top_10_recommended)
    print('Recommended books: ', top_10_recommended[['title', 'review_score', 'sentiment','total_score']])
    print('Reviews noted these books as: ', review_topics)

if __name__ == "__main__":
    main()