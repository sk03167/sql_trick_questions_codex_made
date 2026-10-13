# PySpark verification

Verified 2026-10-13 with PySpark 4.0.1, Python 3.13.12, Java 17.0.12, local[2], ANSI mode enabled and UTC session time zone.

All **191 DataFrame result checks passed** across all 50 exercises. Output column names, row order, NULL values and multiplicities are checked, with a 1e-10 tolerance for floating-point results. The Q01 left-join alternative is also executed.

| Check family | Passed |
| --- | --- |
| Q01 left-join alternative | 6 |
| samples | 50 |
| explicit edge cases | 28 |
| random unordered pairs | 3 |
| random cyclic components | 3 |
| random integer islands | 3 |
| random nested intervals | 3 |
| random union durations | 3 |
| random tied concurrency | 3 |
| random universal coverage | 3 |
| random exact sets | 3 |
| random basket equality | 3 |
| random observation medians | 3 |
| random frequency medians | 3 |
| random adjacent runs | 3 |
| random cyclic descendants | 3 |
| random FIFO allocations | 3 |
| random FIFO valuation | 3 |
| PySpark targeted edges | 12 |
| shuffled inputs across 3 partitions | 50 |

Every original fixture is tested again after shuffling its input rows and repartitioning each input to three partitions. Explicit edge cases are imported from the SQL verifier. Its independent Python graph, interval, set, median and FIFO oracles generate three fixtures per randomized family using seed 20261010. Additional tests cover null final values, decreasing forward fills, empty calendars/graphs, exact FIFO boundaries and a funnel with an invalid early attempt followed by a valid one.

Reproduce with `python verify_pyspark.py --report`. Run `python verify.py` separately for the larger SQLite suite. Spark tests execute the DataFrame API, not the SQLite SQL strings. Only tiny fixtures are collected for assertion. Cluster scaling, Spark Connect, managed cloud runtimes and other Spark versions are not covered by this local run.
