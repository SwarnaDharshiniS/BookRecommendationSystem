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

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a **public** GitHub repo (or a private one if you're on a paid
   Streamlit plan).
2. Go to https://share.streamlit.io, sign in with GitHub, and click "New app".
3. Select your repo/branch and set **Main file path** to `app.py`.
4. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and run the app.
   No extra configuration is needed - the data is already included in `Data/`.

First boot can take a minute or two while dependencies install. If the deploy log shows
an NLTK download error, it usually means the build step has no outbound internet access
temporarily - just restart the app from the Streamlit Cloud dashboard.

## Deploy elsewhere (Render, Railway, a VPS, Docker, etc.)

Any host that can run `pip install -r requirements.txt` and then
`streamlit run app.py --server.port $PORT --server.address 0.0.0.0` will work. There's
no database and no environment variables required - everything the app needs ships in
this folder.

## Known limitations worth knowing about

- The "fiction" genre has ~450k review rows; very generic keywords (like "the") on that
  genre can still take several seconds. The in-app spinner is there so it doesn't look
  frozen, but if you want sub-second responses on that genre specifically, the next step
  would be pre-indexing keywords (e.g. a simple inverted index or a real search engine
  like Whoosh/Elasticsearch) instead of scanning reviews per request.
- This is a single-process, in-memory app with no user accounts or persistence - by
  design, matching the original project's scope (a class project recommendation demo,
  not a production book retailer).
