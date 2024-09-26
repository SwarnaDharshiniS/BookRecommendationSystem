import streamlit as st
from analysis_summary import recommend_book


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

        genre_select = st.selectbox('Please select your preferred genres:',
                                    ['antiques collectibles', 'architecture', 'art', 'bible', 'biography autobiography',
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
                                     'young adult fiction'])

        key_term = st.text_input("Enter a keyword (e.g., 'adventure', 'romance', 'history')")

        if st.button("Recommend"):
            if genre_select and key_term:
                st.write(f"Recommendations for the genre(s): {genre_select}")
                results, topics = recommend_book(genre_select, key_term)
                if results.empty:
                    st.warning("No recommendations found. Try adjusting your preferences.")
                elif results:
                    st.write(results)
                else:
                    st.warning("No recommendations found. Try adjusting your preferences.")
            else:
                st.error("Please select at least one genre and enter a keyword.")

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