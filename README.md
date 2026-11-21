\# Adaptive Pipeline



A benchmark-driven router that chooses between Pandas, DuckDB and Spark

based on data size, file format, operation type and available hardware.



> Work in progress. Started November 2026.



\## Goal



Measure when each engine wins on a single machine, then build a router

that picks the best one automatically, with fallback on memory failure.



\## Planned features



\- \[ ] Three engines behind one interface (Pandas, DuckDB, Spark)

\- \[ ] Benchmark harness (time, peak memory, success/failure)

\- \[ ] Rule-based router with `--explain`

\- \[ ] Evaluation on unseen configurations



\## Status



Step 3: Pandas engine (cleaning done, operations in progress).



\## Limitations



Spark is tested in local mode only (no real cluster).

