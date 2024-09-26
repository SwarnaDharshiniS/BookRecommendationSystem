# Project Document 
## Introduction
### Aims and objectives of the project:
- The aim of this project began with combining education with natural language processing to examine a given subject more closely. This then changed to the narrow subject of books, from the perspective of a student or just for a hobby. The aim then became to analyse book review data given a genre and certain keywords from the user. The objective of this analysis then is to use the language from reviews to summarize topics, semantics and themes within the book and provide a suitable recommendation.
### Roadmap of the report: 
- [Background](#Background)
  - [Overview](#Overview)
  - [Focus](#Focus)
  - [Potential Problems](#Potentialproblems)
  - [Needs](#Needs)
  - [Objectives](#Constraints)
- [Specification and Design](#SpecificationadnDesign)
  - [Requirements](#Requirements)
  - [Design and Architecture](#DesignandArchitecture)
- [Implementation and Execution](#ImplementationandExecution)
  - [Development approach and team member roles](#Developmentapproachandteammemberroles)
  - [Tools and libraries](#Toolsandlibraries)
  - [Implementation Process](#ImplementationProcess)
  - [Agile Development](#AgileDevelopment)
  - [Implementation Challenges](#ImplementationChallenges)
- [Data Collection](#DataCollection)
 - [Results](#Results)
## Background
Any specific details about the project based on your chosen topic. For example: study the factors contributing to air pollution in a given city; identify the common skills and qualifications of the top-performing employees in a company 
### Overview 
Natural language Processing (NLP) describes the field of understanding language within machine learning. This kind of understanding can be used to summarize and describe large amounts of text efficiently and quickly. With this in mind, in Education such a skill is crucial. From research to classroom assistance, we can see how such analysis can help. Within our focus of literature reviews, we are focusing on two uses of NLP in this field:

- Content Analysis:
NLP is used to analyze content like - in our case - book reviews or descriptions and from this analysis we can extract key concepts or themes and provide a summary of the content.

- Personalized Learning:
NLP also has the power of accepting given input to personalise recommendations or content to the given needs of the user. This includes recommendations for reading that adjust to keywords and wants as supplied from the user.

### Focus
Why we narrowed the focus to Books and Review Analysis:

Given the time scale of the project, focusing specifically on books allows us to look at a manageable amount of data whilst providing insightful analysis. Currently, there are millions of books available to users and it can be overwhelming to select our next read which we will enjoy. Hence, we believe the analysis of book reviews using NLP will provide a unique solution to this challenge. Rather than just looking at review scores and previous history for the user, the text within a review provides interesting and nuanced subjective content in which to narrow down recommendations. To do this, we used the branches of NLP mentioned above to:

- Extract key topics from book reviews
- Summarize the sentiment of the review numerically
- Match our findings with the user's needs to provide recommendations

However, knowing where to start with accessing data on books already proved a challenge as this is still such a huge category. We needed a dataset that had enough information to provide quality results without overloading the computer when trying to read this data. Once we found a suitable dataset, the project started to come together and we felt strong with the amount of data we had available and how we managed that e.g. by filtering data.

### Potential problems
- Information overload: with such a volume of books we have in the modern day, as mentioned, it may be difficult to manage such a dataset which attempts to describe all of these datapoints.
- Book reviews are subjective: The points of interest for a book for one person may be very different for another and how we may describe said book may vary, this may result in unhelpful data for our users.

### Needs
- Dealing with data: We need to deal with large amounts of data. To do this we may potentially filter it based on genre and pick out reviews given topics. This requires use of the pandas library and scikit.
- Analyze the Content of Reviews: We must provide meaningful insight from the reviews we look at using sentiment, key topics etc. To visualise and analyse this information further we may also need matplotlib and numpy.
- User Input: We must provide an interface for the user and be able to collect input like keywords and genre to find a recommended book for the user.
- Generate Personalized Recommendations: Use the analysis and user input to provide suggestions.

## Specification and Design
### Requirements 
- **Technical Requirements:**
  - **API use:** The system must use an API like Google Books API or Kaggle API to fetch reviews for a data frame which can then be analysed.
  - **NLP Tools:** Implementation of NLP libraries like NLTK to analyze text from reviews. This includes tools for topic modeling and sentiment analysis to extract key topics and provide sentiment scores.
  - **Data Storage:** A method of storing data which is easy to access and update using CSV files.
  - **User Interface (UI):** A web-based or desktop interface to select genres and input keywords and receive recommendations.
  - **Recommendation System:** An algorithm to match user inputs with analysis data to select recommendations.
  - **Efficiency/Performance:** The system must handle large volumes of data efficiently and analyze thousands of reviews.
 - **Non-Technical Requirements:**
   - **User Accessibility:** The system should be user-friendly and intuitive for users. This includes making simple buttons and input boxes and instructions.
   - **Documentation:** Comprehensive documentation covering system setup and usage. This includes an about page on UI.
### Design and Architecture
 - **Data Collection:** Review Aggregation - A component responsible for fetching and merging book review data from various sources within the Kaggle API. 
 - **Data Processing:** This includes both preprocessing - removing stopwords, removing capital etc., -  and sentiment analysis and topic modeling. The results from these processes are then ready for analysis.
 - **Recommendation Engine:** Takes user inputs (genre, keywords) and matches them with the processed review data to generate recommendations. It matches this data using insights from the NLP module to rank and select the best suited books.
 - **User Interface:**

   Frontend: The UI where users interact with the program. This includes forms for genre and keywords and then displays the recommended books and may also include insights like themes and sentiments and the relationships between this data.
   Backend: The communication layer between the frontend and the backend program. This process handles requests from the UI and reports them to the recommendation engine returning the results to the user.
   
## Implementation and Execution
### Development approach and team member roles
**Development Approach:**

Throughout the project we aimed to follow a scrum still software development cycle. To implement this we had regular meetings loosely structured around sprint plans and reviews where we discussed the next period of work we were aiming to have finished by the next meeting and demonstrated the work each of us had completed. Everyone attended these meetings and Eva acted as scrum master. At each meeting we brainstormed ways in which we could make our development more efficient whether that was in the way we dealt with the data to using software like Trello to keep on top of tasks. The meetings roughly covered the following:
1. 26/07 - Decide Group project topic and have a discussion on project assignment. Start building a design of the project and how it may be structure.
2. 11/08 - Discuss project focus and management for the Semantic Book Recommendation System. Adapt project to requirements given.
3. 15/08 - Data has been gathered from Kaggle API and some topic modelling tested on data. Need to restrict dataset to make more manageable.
4. 22/08 - Completion and review of work done so far: sentiment analysis, UI, compliation of modules and files etc., and discussion regarding our testing strategy.

**Team Member Roles:**

 - Srivatsala: Backend developer (handled database interactions and interactions with API)

 - Wing Hang: Data Visualisation (used the data from the NLP to create visualisations which emphasise the relationships between data)

 - Swarna: Frontend Developer (oversaw the user interface), handled NLP in sentiment analysis

 - Eva: Project Manager (organised meetings and the project timeline), handled NLP in topic modelling

### Tools and libraries
**Programming Languages:**

Throughout the project Python was used with the utilization of the following libraries:

 - NLP Libraries: NLTK was used for the sentiment analysis utilizing vader lexicon, sklearn was used in the topic modelling file to create a term document matrix and fuzzywuzzy was used when searching up keywords within the topics found in topic modelling to find words similar to the given keywords.
 - Web Frameworks: Streamlit was used for the user interface.
 - Visualization Tools: Seaborn, Matplotlib and Numpy were used for visualisation to manipulate data and create informative graphs.

**Development Tools:** 

To compile documents and utilize version control we used GitHub and for our task management we used Trello. 

### Implementation Process

**Achievements:**
 - Dealing with such a large dataset and successfully cleaning the data and splitting it into more manageable datasets.
 - Completing the NLP with relatively few obstacles - this was a particularly difficult part of the project which we had less experience with.

**Challenges:**
 - The biggest challenge with implementation was the large amount of data we had so we had to adapt to this early and keep changing our code throughout to ensure it was running efficiently along with the data. We also found the dataset we used did not have ISBN on all data frames so we had to merge using the title of books instead. This presented a challenge with ensuring the data was normalized correctly and two different titles weren't merged together but agreed on a comprise of this standard to ensure we had enough data to extract informative analysis. 

### Agile Development

**Agile Elements used:**
Within the implementation process, we used agile techniques like iteration and ensured to keep revisiting code once we had created new modules and files to interact with it to test interaction and modify issues creating a smoother process and resulting in changes in data management and analysis. We also each reviewed the other's code to ensure quality and cohesive practice. Our regular team meetings also enable us to quickly discuss any progress or obstacles.

**Impact of Agile:**
Using agile enabled us to stay on the timeline and immediately address issues such that any obstacles could be efficiently addressed and adapted to. This also meant we could see improvement quickly and eased any concerns of meeting the deadline.

### Implementation Challenges

**Technical Challenges:**
We initially had issues with using the data in the NLP modules of code as it was such a large file but after filtering the data by genre this problem was largely improved on and we could receive results on data processing much more quickly. 

**Resource and Time Management Challenges:**
Within such  tight timeline we knew we had to keep the project to a minimum to ensure we could meet our objectives. To address this we ranked tasks in terms of importance and made sure we had completed the crucial elements of the project first. 

**Testing:**

Ran testing with pytest and only key issue was with case where no books could be recommended due to strange keywords being used or overly specifickeywords being used. This was rectified by modifying the book_recommend function

## Data Collection
### Information needed

 - Book Titles and Authors: Basic metadata for categorization.
 - Genres: To categorize books and filter reviews according to user preferences.
 - Review Text: The actual content of user reviews or a short summary. This is the text which will be analyzed using NLP techniques to extract sentiments and key topics.
 - Ratings: Numerical or star-based ratings provided by users, which is used alongside the NLP analysis to rank books and which is used to compare with the sentiment score each review is given.
   
### Available information

 - Publicly Available Reviews: This includes from platforms like Goodreads or Amazon with the former having an API that is unaccessible for free.
 - Book Metadata: Details like publication date, publisher, genre, and book description, accessible through API's like Google
 - Aggregated User Ratings: Platforms like Kaggle provide aggregate ratings that summarize user feedback.

### Data source

 - APIs of Book Review Platforms: As mentioned platforms Google books API and the Kaggle API allow programmatic access to their data.

### Method of Data Collection

**API Usage:**
 - Selected API: We selected Kaggle API for data collection.
 - Functionality: The Kaggle API allows users to interact with Kaggle - a platform which provides datasets. This API provides allows you to manage Kaggle datasets, notebooks, and other resources, from a terminal or script.
 - Data Retrieval: A key was created and Kaggle library was installed onto the terminal. The environment variables were set and authenticated and the the URL for the dataset is given allowing it to be downloaded. 
**Data Cleaning and Preprocessing:**
 - Data Formatting: Unnecessary columns were dropped and spaces in text and inconsistency were modified. Lastly, column titles were changed to the same format and missing values were handled. 
 - Normalization: The dataset was already normalized apart from redundant data.

## Results
### Overview of Key Findings
 - **Alignment with Objectives:** A book recommendation system was created and we were able to spot some patterns in the book data which may assist in understanding why certain books receive a better reception.
 - **Recommendation Results:** Books were recommended given the keywords weren't overly specific and were in normal text. 10 recommendations were given and these were ranked.
 - **Topic Analysis:** A couple of genres were explored in more detail and once the generic language was filtered a few interesting topics were found as frequently occurring. For example:
    - Architecture - reference, history, resource, classic.
    - Foreign Language Studies - dictionary, expectations, classic, useful.
    - Young Adult Fiction - classic, love, wonderful, edition.
   Interestingly in literary criticism, words like Jane Eyre and Tom Sawyer came up a lot perhaps out of comparison or representative of a huge volume of criticisms of these novels.
   The correlations between topics and ratings were less informative as words like 'good' and 'great' had some positive correlation with good ratings as to be expected.
 - **Sentiment Analysis:** Regarding the distribution of sentiment, there was a large skew towards positive sentiments with positive sentiment scores correlating with positive ratings. Regarding negative ratings, there was much more variation in sentiment score.
 - **Book Data Analysis:** Ratings were largely found to be positive with no particular relationship between book length and ratings. Routledge was the leading publish company regarding number of positive ratings whilst National Geographic had the highest average rating. This result may be due to a higher volume of books from Routledge which have been reviewed by Amazon customers. Within book genres, Juvenile Fiction received the highest average ratings. and Computers had the largest variation of ratings.
 - **Limitations of the Results:** We were not able to specify the Fiction category into further subgenres and so the data for this file may be less accurate and provide more general recommendations. We were also not able to rank books by the density of given keywords in their reviews. This function may have resulted in more accurate personal reviews. 

## Conclusion
The book recommendation system was successfully implemented with some helpful and interesting data surrounding the reviews and sentiments. To further improve on this, more detailed information could be extracted with density of keywords and subgenres etc., A more efficient way of handling such a large dataset could also be sought but due to the short timeframe in which this project was completed we have managed well with the methods we have used.
