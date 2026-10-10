# SQL Catalog Verification

Verified on October 10, 2026 with Python 3.14.7 and SQLite 3.53.4.

All 1993 query checks passed. Every primary solution and documented alternative was executed in a fresh in-memory database and compared with independent expected rows. Embedded document SQL was checked against the executable files. Internal document file and heading links were checked.

| Check family | Passed query checks |
| --- | --- |
| samples | 50 |
| alternatives | 8 |
| explicit edge cases | 35 |
| random unordered pairs | 200 |
| random cyclic components | 100 |
| random integer islands | 200 |
| random nested intervals | 100 |
| random union durations | 100 |
| random tied concurrency | 100 |
| random universal coverage | 200 |
| random exact sets | 100 |
| random basket equality | 100 |
| random observation medians | 100 |
| random frequency medians | 100 |
| random adjacent runs | 200 |
| random cyclic descendants | 100 |
| random FIFO allocations | 100 |
| random FIFO valuation | 100 |

Randomized fixtures use seed 20261010 with 100 generated cases per selected family. Python reference oracles independently normalize pairs, traverse graphs, merge intervals, count concurrency, compare sets, compute medians, detect runs, and simulate FIFO consumption. Alternative solutions are also checked when present in a tested family.

Explicit cases include empty inputs, an empty required product set, a singleton root, self cycles, no qualifying children, all-NULL values, the exact inactivity threshold, a fully occupied time window, capacity overflow at the first person, and a fully consumed FIFO product.

Run `python3 verify.py` to reproduce the full verification; use `--question Q13` to focus on one exercise. A focused run does not overwrite this full-run report.

These checks verify the reference dialect and declared contracts. They are not execution tests for PostgreSQL, SQL Server, MySQL, or Spark SQL, not a proof for all possible inputs, and not performance benchmarks. SQLite permits some expressions that stricter engines reject, so translation still needs engine-specific review and execution.
