# Book Recommendation System

A Streamlit app that recommends books by genre and keyword, ranked using sentiment
analysis of Amazon book reviews plus topic modeling of the top results.

## ⚠️ Security note - rotate your Kaggle API key

The original repo's `Data.zip` contains `Data/Data Collection/Kaggle Dataset/kaggle.json`
with a **real Kaggle username and API key committed in plain text**. Since the repo is
public on GitHub, that key is exposed to anyone. Please:
1. Go to your Kaggle account settings and **revoke/regenerate** that API token now.
2. Remove `kaggle.json` from the repo (and ideally scrub it from git history, e.g. with
   the `git filter-repo` or BFG tool, since old commits still contain it even if you
   delete the file going forward).

This package leaves that file out entirely - it isn't needed to run the app.

## What was wrong / what was fixed

1. **App crashed on every successful recommendation.** `app.py` did `elif results:`
   on a pandas DataFrame, which raises `ValueError: The truth value of a DataFrame is
   ambiguous` any time results were found - i.e. the app's main feature crashed every
   time it worked. Fixed to just use `else`.
2. **Selecting "self-help" crashed the app.** There's no `self-help_df.csv` in the
   data, but the genre was in the dropdown, causing an unhandled `FileNotFoundError`.
   `recommend_book` now raises that error clearly, and `app.py` catches it and shows a
   friendly message instead of crashing.
3. **No `requirements.txt`.** The project couldn't actually be installed/deployed.
   Added one with the libraries the code uses (`streamlit`, `pandas`, `scikit-learn`,
   `nltk`, `fuzzywuzzy`, `python-Levenshtein`).
4. **Severe slowness on common keywords.** Matching used `DataFrame.iterrows()` plus a
   fuzzy-match check against every word of every review, even for exact matches. On the
   "fiction" genre (~450k reviews) a simple query took 30-50+ seconds. Now there's an
   exact-match fast path, a cheap mathematical pre-filter that skips fuzzy comparisons
   that can't possibly reach the match threshold, and `itertuples()` instead of
   `iterrows()`. Same matching behavior (typos/close variants still match), ~7x faster
   in the worst case tested.
5. **Repeated disk reads.** Every recommendation reloaded the full genre CSV from disk.
   Genre data is now cached in memory per process.
6. **Topic modeling bugs.** `CountVectorizer(max_df=1, ...)` only kept words that
   appeared in exactly one document, which could throw "empty vocabulary" and crash the
   page; `display_topics` also had a `return` inside its loop that meant it only ever
   reported the first of 5 topics. Both fixed, with a friendly fallback string if there
   genuinely isn't enough review text to model.
7. **Noisy/fragile NLTK download.** `sentiment_analysis.py` called `nltk.download(...)`
   unconditionally on every import. It now checks if the data is already present first,
   and raises a clear error if a download is needed but fails (e.g. no internet).
8. Minor UX: added a loading spinner (queries can take a few seconds on large genres),
   a cleaner results table, and an expandable section to read full review excerpts.

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
