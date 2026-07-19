# Book Recommendation System

A Streamlit app that recommends books by genre and keyword, ranked using sentiment
analysis of Amazon book reviews plus topic modeling of the top results.

## Project structure

```
.
├── app.py                  # Streamlit UI
├── analysis_summary.py     # keyword matching + orchestration
├── sentiment_analysis.py   # VADER sentiment scoring
├── topic_modeling.py       # LDA topic summary of top results
├── Genre_filter.py         # one-off script used to build the per-genre CSVs (not needed at runtime)
├── test_recommendations.py # pytest suite
├── requirements.txt
└── Data/
    └── filtered_reviews/   # one CSV per genre (already extracted, ready to use)
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501. The first run will download the small NLTK
`vader_lexicon` package (a few hundred KB) if it isn't already cached on your machine.

Run the test suite with:

```bash
pip install pytest
pytest test_recommendations.py -v
```
