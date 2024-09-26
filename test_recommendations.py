import pytest
import pandas as pd
from analysis_summary import recommend_book

# check that the program works with expected input
def test_normal_input():
    user_preferences = {
        "preferred_genre": "travel",
        "preferred_keywords": "adventure epic"
    }
    genre = user_preferences['preferred_genre']
    key_term = user_preferences['preferred_keywords']

    recommendations, topics = recommend_book(genre, key_term)

    # Check that the recommended books are from the preferred genres
    assert all(genre == "travel" for genre in recommendations['categories'])

    # This part is difficult as uses machine learning to find similar keywords, so return a list of reviews
    # from said book to check ourselves
    recommended_reviews = recommendations['review_summary'].tolist()
    return recommended_reviews


# Edge case: No books match
def test_no_matching_books():

    user_preferences = {
        "preferred_genre": "antiques collectibles",
        "preferred_keywords": "Mary Jane"
    }

    genre = user_preferences['preferred_genre']
    key_term = user_preferences['preferred_keywords']

    recommendations, topics = recommend_book(genre, key_term)
    assert recommendations.empty

# Edge case: simple words inputted so any book matches
def test_all_books_match():

    user_preferences = {
        "preferred_genre": "fiction",
        "preferred_keywords": "the a"
    }

    genre = user_preferences['preferred_genre']
    key_term = user_preferences['preferred_keywords']

    recommendations, topics = recommend_book(genre, key_term)

    # Check that still only 10 books are recommended
    assert len(recommendations) == 10

# Test for Case Sensitivity
def test_case():

    user_preferences_one = {
        "preferred_genre": "humor",
        "preferred_keywords": "Funny"
    }

    user_preferences_two = {
        "preferred_genre": "humor",
        "preferred_keywords": "funny"
    }

    genre = user_preferences_one['preferred_genre']
    key_term_one = user_preferences_one['preferred_keywords']
    key_term_two = user_preferences_two['preferred_keywords']

    recommendations_one, topics_one = recommend_book(genre, key_term_one)
    recommendations_two, topics_two = recommend_book(genre, key_term_two)

    # Convert titles to lists and sort them before comparing
    titles_one = sorted(recommendations_one['title'].tolist())
    titles_two = sorted(recommendations_two['title'].tolist())

    assert titles_one == titles_two

#test with invalid inputs
def test_invalid_input():
    user_preferences = {
        "preferred_genre": "travel",
        "preferred_keywords": "12345"
    }
    genre = user_preferences['preferred_genre']
    key_term = user_preferences['preferred_keywords']

    recommendations, topics = recommend_book(genre, key_term)

    # Check that no book recommended
    assert recommendations.empty
