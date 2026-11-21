# Devlog

## 2026-11-17: Repository setup
- Created a public GitHub repo (`adaptive-pipeline`) with README, Python .gitignore and MIT license; cloned it locally and tested cloning it in Colab.
- Folder layout: `src/adaptive_pipeline/` (with `engines/`), `tests/`, `notebooks/`, `docs/`, `data/`, `results/`.
- Added data rules to `.gitignore` (raw/processed data and benchmark CSVs are never committed) and a `requirements.txt`.
- Decisions: dataset is NYC Yellow Taxi; project scope is a benchmark-driven router choosing between Pandas, DuckDB and Spark (not just Pandas vs Spark); README status is tracked by steps, not weeks.

## 2026-11-18: Data exploration (`notebooks/01_explore.ipynb`)
- Data: Jan 2024 yellow taxi, Parquet, 2,964,624 rows.
- File size vs memory: 50.0 MB on disk -> 535.9 MB in memory (10.7x).
- One text column (`store_and_fwd_flag`) used 144.6 MB (~27% of all memory). Converting it to `category` gave 2.96 MB.
- `passenger_count` float64 -> Int8: 23.72 MB -> 5.93 MB
- Reading only 4 needed columns takes 94.9 MB instead of 535.9 MB.
- Data quality (per rule): duration outside 1-180 min 37,104 rows (1.25%); distance == 0 60,371 (2.04%); fare <= 0 38,341 (1.29%). Rules overlap: individual counts sum to 135,816 but combined unique rows are 105,602 (3.56%).
- Takeaway: memory cannot be estimated from file size alone; it depends on columns read and dtypes.

## 2026-11-19: Local environment
- Installed pandas, pyarrow, pytest. Local pandas is 3.1.0 (Colab version: 2.2.3); results may differ across versions, so versions will be logged in benchmarks.
- Added `pyproject.toml` with `pythonpath = ["src"]` so pytest can import the package.

## 2026-11-21: Pandas `clean()` function and tests
- Wrote `clean(df)` in `pandas_engine.py`. It keeps rows where duration is 1-180 min (both ends included), `trip_distance > 0`, `fare_amount > 0`. It does not modify its input and returns the same columns.
- Missing values are dropped implicitly.
- Worked test-first: started with a stub that returns the input unchanged, wrote tests, watched them fail, then implemented.
- Test design lesson: each invalid row should break only ONE rule, otherwise removing a rule can go unnoticed. Boundary rows (exactly 1 and 180 min) are tested explicitly.
- pytest result: All 4 tests are passed for the example "CASES" dataframe.
- Rule-removal experiment (delete one rule, confirm a test fails): expected tests failed for each removal.
- Validated `clean()` on the full January file (Colab, pandas 2.2.3): 2,964,624 -> 2,859,022 rows; 105,602 removed, exactly the combined count from the exploration step.
