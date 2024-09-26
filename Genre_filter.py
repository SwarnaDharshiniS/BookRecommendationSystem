import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

#I've added this function as previously some of the text for genres was not fully processed and wouldn't match
# any of the genres I had listed - this takes the text and removes words like 'and', removes capitals, commas etc.,
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

#I'm using the large file we have and trying to split it into the following genres - the genres were chosen
# as previously the file had many very niche genres and so I chose those with the large amounts of books within
#that genre in order to be able to explore the data fully
reviews_df = pd.read_csv('Data/books_and_reviews.csv', usecols=['title', 'categories', 'review_summary',
                                                                'review_score', 'publisher'])

reviews_df['categories'] = reviews_df['categories'].apply(preprocess_text)

category_list = ['antiques collectibles', 'architecture', 'art', 'bible', 'biography autobiography',
                 'body mind spirit', 'business economics', 'comics graphic novels',
                 'computers', 'cooking', 'crafts hobbies', 'design', 'drama', 'education', 'family relationships',
                 'fiction', 'foreign language study', 'games', 'gardening', 'health fitness', 'history',
                 'house home', 'humor', 'juvenile fiction', 'juvenile nonfiction', 'language arts disciplines',
                 'law', 'literary collections', 'literary criticism', 'mathematics', 'medical', 'music', 'nature',
                 'performing arts', 'pets', 'philosophy', 'photography', 'poetry', 'political science', 'psychology',
                 'reference', 'religion', 'science', 'self-help', 'social science', 'sports recreation', 'study aids',
                 'technology engineering', 'transportation', 'travel', 'true crime', 'young adult fiction']

#first group the genres
grouped = reviews_df.groupby('categories')

# Next loop through the genres we've listed and the groups matching genres and saving dataframes
for genre in category_list:
    for group_name, group_df in grouped:
        if group_name == genre:
            filename = f"{group_name}_df.csv"
            group_df.to_csv(filename, index=False)
            print(f"Saved {filename}")
