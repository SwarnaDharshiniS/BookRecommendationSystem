import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

#download vader lexicon which analyses the sentiment of the text and creates an instance of an nltk class which uses vader
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

'''
takes text as input and returns one of 4 sentiment scores: negative, positive, neutral or compound (normalized score which summarizes sentiment from
-1 to 1.
'''
def analyze_sentiment(review_text):
    sentiment_score = sia.polarity_scores(review_text)
    return sentiment_score['compound']  # Compound score as overall sentiment measure

def apply_sentiment_analysis(reviews_df):
    # processes each review and applies the get_sentiment function
    #reviews_df['sentiment'] = reviews_df['review_summary'].fillna('')
    reviews_df['sentiment'] = reviews_df['review_summary'].apply(analyze_sentiment)
    return reviews_df

def main():
    reviews_df = pd.read_csv('Data/filtered_reviews/architecture_df.csv')
    sentiment_df = apply_sentiment_analysis(reviews_df)

    # Example: Print out the sentiment results
    print(sentiment_df[['title', 'sentiment']].head())


if __name__ == "__main__":
    main()