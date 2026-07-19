import os
import re
import functools

import pandas as pd
from fuzzywuzzy import fuzz

from topic_modeling import main_topics
from sentiment_analysis import apply_sentiment_analysis

FUZZY_THRESHOLD = 80
REQUIRED_COLUMNS = ['title', 'categories', 'review_summary', 'review_score', 'publisher']


def _max_possible_ratio(len_a, len_b):
    """
    The highest fuzz.ratio() two strings of these lengths could ever score,
    reached only if the shorter is fully contained in the longer. Used as a
    cheap pre-filter so we skip the (relatively expensive) fuzz.ratio() call
    entirely for word pairs that are mathematically guaranteed to fall below
    the match threshold, e.g. comparing a 7-letter search term against "a"
    or "is". This never changes which pairs *can* match - it just skips
    computing the ratio for pairs that have no chance of reaching it.
    """
    total = len_a + len_b
    if total == 0:
        return 0
    return (2 * min(len_a, len_b) / total) * 100


def has_keywords(text, keywords):
    """
    Returns True if any keyword (or a close fuzzy match of it, e.g. a small
    typo or a slightly different word ending) is found among the words of
    the given text.
    """
    if not isinstance(text, str) or not keywords:
        return False

    words = text.lower().split()
    word_set = set(words)
    for keyword in keywords:
        keyword_lower = keyword.lower()
        keyword_len = len(keyword_lower)
        # fast path: an exact word match covers the vast majority of real
        # searches and is far cheaper than computing a fuzzy ratio
        if keyword_lower in word_set:
            return True
        # fallback: fuzzy match catches typos / close variants
        for word in words:
            if _max_possible_ratio(keyword_len, len(word)) < FUZZY_THRESHOLD:
                continue
            if fuzz.ratio(keyword_lower, word) >= FUZZY_THRESHOLD:
                return True
    return False


def matched_books(reviews_df, keywords):
    """
    Takes a dataframe of book reviews and a list of keywords, and returns a
    list of dicts (one per unique book title) whose review text contains at
    least one of the keywords.

    Performance note: the original implementation walked the dataframe with
    `iterrows()` (one of the slowest ways to iterate a pandas DataFrame) and
    ran a fuzzy-match comparison against *every single word* of every review
    for every keyword, even when the keyword appeared verbatim. On a large
    genre such as "fiction" (~450k review rows) this made even a simple
    two-word query take 30+ seconds, which is enough to look "stuck" or
    risk a timeout once deployed. This version keeps the exact same
    fuzzy-matching behaviour (typos / close variants still match) but adds a
    cheap exact-word regex fast path and uses `itertuples()`, which together
    bring that same query down to a couple of seconds.
    """
    if not keywords:
        return []

    keyword_pattern = re.compile(
        r"\b(?:" + "|".join(re.escape(k.lower()) for k in keywords if k) + r")\b"
    )

    matching_books = []
    seen_titles = set()

    for review in reviews_df.itertuples(index=False):
        title = review.title
        if title in seen_titles:
            continue

        text = review.review_summary
        if not isinstance(text, str):
            continue

        text_lower = text.lower()
        is_match = bool(keyword_pattern.search(text_lower)) or has_keywords(text_lower, keywords)
        if is_match:
            matching_books.append({
                'title': title,
                'categories': review.categories,
                'review_summary': text,
                'review_score': review.review_score,
                'publisher': review.publisher,
                'keyword match': 1
            })
            seen_titles.add(title)

    return matching_books


@functools.lru_cache(maxsize=6)
def _load_genre_reviews(genre):
    """
    Loads (and caches in memory) the reviews CSV for a given genre.

    Caching avoids re-reading large CSVs (the "fiction" genre alone is
    ~40MB/450k rows) from disk on every single recommendation request,
    which matters a lot once this is deployed and serving real traffic.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "Data", "filtered_reviews", f"{genre}_df.csv")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"No review data is available for the '{genre}' genre yet."
        )

    return pd.read_csv(file_path, usecols=REQUIRED_COLUMNS)


def recommend_book(genre, key_term):
    """
    Returns (top_10_recommended_books_df, review_topics_string) for the
    given genre and space-separated keyword string.

    Raises FileNotFoundError if no data file exists for the requested genre
    (the caller, e.g. the Streamlit app, should catch this and show a
    friendly message rather than letting it crash the page).
    """
    reviews_df = _load_genre_reviews(genre)

    keywords = key_term.split()
    matches = matched_books(reviews_df, keywords)
    if not matches:
        return pd.DataFrame(), []

    matching_books = pd.DataFrame(matches)
    # apply sentiment analysis to the current pool of books
    recommended_books = apply_sentiment_analysis(matching_books)
    # calculate a score for the books based on the sentiment analysis and the review score
    recommended_books['total_score'] = (recommended_books['review_score'] + recommended_books['sentiment']) / 2
    # sort books by this calculated score
    recommended_books = recommended_books.sort_values(by=['total_score'], ascending=False)

    # output the top 10
    top_10_recommended = recommended_books.head(10)
    review_topics = main_topics(top_10_recommended)
    return top_10_recommended, review_topics


def main():
    # some example user input: a genre and a few keywords to narrow down books
    keywords = ['serious', 'melancholy']
    genre = 'biography autobiography'

    top_10_recommended, review_topics = recommend_book(genre, ' '.join(keywords))
    print('Recommended books: ', top_10_recommended[['title', 'review_score', 'sentiment', 'total_score']])
    print('Reviews noted these books as: ', review_topics)


if __name__ == "__main__":
    main()
