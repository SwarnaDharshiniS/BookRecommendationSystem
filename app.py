import streamlit as st
from analysis_summary import recommend_book


GENRES = [
    'antiques collectibles', 'architecture', 'art', 'bible', 'biography autobiography',
    'body mind spirit', 'business economics', 'comics graphic novels', 'computers',
    'cooking', 'crafts hobbies', 'design', 'drama', 'education',
    'family relationships',
    'fiction', 'foreign language study', 'games', 'gardening', 'health fitness',
    'history', 'house home', 'humor', 'juvenile fiction', 'juvenile nonfiction',
    'language arts disciplines', 'law', 'literary collections', 'literary criticism',
    'mathematics', 'medical', 'music', 'nature', 'performing arts', 'pets',
    'philosophy',
    'photography', 'poetry', 'political science', 'psychology', 'reference',
    'religion',
    'science', 'self-help', 'social science', 'sports recreation', 'study aids',
    'technology engineering', 'transportation', 'travel', 'true crime',
    'young adult fiction'
]


def show_recommendations(genre_select, key_term):
    try:
        with st.spinner(f"Looking for '{key_term}' books in {genre_select}..."):
            results, topics = recommend_book(genre_select, key_term)
    except FileNotFoundError:
        # Happens if a genre is selected that has no matching data file yet
        st.error(
            f"Sorry, there's no review data available for the '{genre_select}' "
            "genre yet. Please try a different genre."
        )
        return

    if results.empty:
        st.warning("No recommendations found. Try adjusting your genre or keyword.")
        return

    st.success(f"Found {len(results)} recommendation(s) for '{genre_select}'.")

    display_columns = {
        'title': 'Title',
        'publisher': 'Publisher',
        'review_score': 'Review score',
        'sentiment': 'Review sentiment',
        'total_score': 'Overall score',
    }
    display_df = results[list(display_columns.keys())].rename(columns=display_columns)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if topics:
        st.subheader("Common themes in these reviews")
        st.write(topics)

    with st.expander("Show review excerpts"):
        for _, row in results.iterrows():
            st.markdown(f"**{row['title']}**")
            st.write(row['review_summary'])
            st.divider()


def main():
    st.title('Book Recommendation System')
    menu = ["Home", "Recommend", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the Book Recommendation System")
        st.write("""
                Discover books tailored to your interests! Use the 'Recommend' section to select a genre and enter keywords to get personalized book suggestions.

                **How to Use This App:**

                1. Navigate to the 'Recommend' tab from the sidebar.
                2. Select your preferred genre from the dropdown menu.
                3. Enter a keyword that interests you (e.g., 'adventure', 'romance').
                4. Click the 'Recommend' button to see a list of books tailored to your preferences.

                Explore different genres and discover your next favorite read! Enjoy!
                """)

    elif choice == "Recommend":
        st.subheader("Get Your Book Recommendations")

        genre_select = st.selectbox('Please select your preferred genre:', GENRES)
        key_term = st.text_input("Enter a keyword (e.g., 'adventure', 'romance', 'history')")

        if st.button("Recommend"):
            if genre_select and key_term:
                show_recommendations(genre_select, key_term)
            else:
                st.error("Please select a genre and enter a keyword.")

    else:
        st.subheader("About")
        st.write("""
                This book recommendation system was developed as part of the CFG Degree Summer 2024 group project.
                Our aim is to provide users with personalized book suggestions based on their interests and preferences.
                We hope you find your next great read!

                **Project Team Members:** 
                - Eva Morris
                - Wing Hang
                - Srivatsala K A
                - Swarna Dharshini S
            """)


if __name__ == '__main__':
    main()
