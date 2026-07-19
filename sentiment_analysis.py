import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def _ensure_vader_lexicon():
    """
    Makes sure the VADER lexicon is available before it's used.

    The original code called nltk.download('vader_lexicon') unconditionally at
    import time. That re-checked the network on every single app restart/reload
    and offered no graceful failure path if the machine had no internet access
    at that moment (common on first deploy / restricted networks). Here we only
    download when the data is actually missing, and we surface a clear error if
    the download itself fails instead of letting a cryptic LookupError bubble up
    from deep inside nltk later on.
    """
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        try:
            nltk.download('vader_lexicon', quiet=True)
        except Exception as exc:
            raise RuntimeError(
                "Could not download the NLTK 'vader_lexicon' resource needed for "
                "sentiment analysis. Check the deployment environment's internet "
                f"access. Original error: {exc}"
            ) from exc


_ensure_vader_lexicon()
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(review_text):
    """
    Takes text as input and returns the VADER compound sentiment score
    (an overall measure from -1 (negative) to 1 (positive)).
    """
    if not isinstance(review_text, str) or not review_text.strip():
        return 0.0
    sentiment_score = sia.polarity_scores(review_text)
    return sentiment_score['compound']


def apply_sentiment_analysis(reviews_df):
    # processes each review and applies the get_sentiment function
    reviews_df = reviews_df.copy()
    reviews_df['sentiment'] = reviews_df['review_summary'].apply(analyze_sentiment)
    return reviews_df


def main():
    reviews_df = pd.read_csv('Data/filtered_reviews/architecture_df.csv')
    sentiment_df = apply_sentiment_analysis(reviews_df)

    # Example: Print out the sentiment results
    print(sentiment_df[['title', 'sentiment']].head())


if __name__ == "__main__":
    main()
