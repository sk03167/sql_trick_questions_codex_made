# SQL Trick Question Catalog

50 exercises organized into 25 patterns, with fresh datasets, expected outputs, and runnable solutions.

- [Questions and sample datasets](QUESTIONS.md)
- [Solutions and explanations](SOLUTIONS.md)
- [Verification results](VERIFICATION.md)

The focus is reverse-pair deduplication, gaps and islands, nested intervals, temporal joins, anti joins, join multiplicity, relational division, window frames, rolling distinctness, medians, recursion, ordered funnels, and FIFO. Simple count questions and ordinary top-earner ranking exercises are excluded. Some solutions use COUNT or ROW_NUMBER as building blocks; their challenge is the surrounding semantics.

## Practice and verification

Use Python 3 with SQLite 3.28 or newer:

```sh
python3 verify.py
python3 verify.py --question Q13
```

To run a query manually, load its setup and solution into a fresh SQLite database:

```sh
sqlite3 :memory: '.read sql/Q13_setup.sql' '.read sql/Q13_solution.sql'
```

There are two main study documents. The sql folder contains extracted executable copies, catalog.json holds structured metadata and independent expected rows, build_catalog.py generates the documents, and verify.py checks queries and randomized edge cases. These support reproducibility without requiring a server or package install. Do not load all setup files into one database; exercises intentionally reuse table names.

Read the [dialect notes](SOLUTIONS.md#dialect-and-data-conventions) before translating queries to SQL Server, PostgreSQL, MySQL, or Spark SQL. Calendar and elapsed-time ordinals make the algorithm explicit. Actual DATE/TIMESTAMP conversions need the correct dialect and timezone.

## Research and scope

Researched on October 10, 2026. This is a curated catalog rather than a claim to enumerate every SQL puzzle on the internet. Questions were selected for a distinct conceptual trap, not merely a long query. Similar variants are included only when the additional condition changes the solution, such as set containment versus equality, row adjacency versus consecutive IDs, or interval packing versus complement and duration.

Public challenge pages, original author tutorials, and official database documentation provide the pattern references. Each exercise identifies whether it adapts a published problem or is an original extension/semantics exercise. All fixtures and solution prose are newly authored; source datasets and editorials are not copied. No employer attribution or claim of interview frequency is inferred. Some other LeetCode pages encountered during research required a subscription and were not used as verified problem statements.

Official documentation linked for an original exercise establishes the SQL construct or semantics; it does not claim that the exact exercise appeared in an interview. Verification covers the declared sample and targeted generated cases, not every possible input or production performance. Closest-match and correlated-window reference solutions prioritize clarity over scale.

## Source references

- [LeetCode Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/)
- [LeetCode Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/)
- [Itzik Ben Gan Closest Match Part 1](https://sqlperformance.com/2018/12/t-sql-queries/closest-match-part-1)
- [LeetCode Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/)
- [SQLite SQL Expressions](https://www.sqlite.org/lang_expr.html)
- [Kathi Kellenberger FIFO Stock Inventory](https://www.red-gate.com/simple-talk/databases/sql-server/performance-sql-server/set-based-speed-phreakery-the-fifo-stock-inventory-sql-problem/)
- [LeetCode Friend Requests II](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/)
- [LeetCode Investments in 2016](https://leetcode.com/problems/investments-in-2016/)
- [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/)
- [HackerRank Symmetric Pairs](https://www.hackerrank.com/challenges/symmetric-pairs/problem)
- [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [PostgreSQL Recursive Queries](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html)
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/functions-window.html)
- [LeetCode Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/)
- [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem)
- [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html)
- [LeetCode Restaurant Growth](https://leetcode.com/problems/restaurant-growth/)
- [LeetCode Exchange Seats](https://leetcode.com/problems/exchange-seats/)
- [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html)
- [Ryan Guill Aggregating event data into sessions](https://ryanguill.com/postgresql/sql/2024/06/24/aggregating-event-data-into-sessions.html)
- [LeetCode Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/)
- [Itzik Ben Gan Matching Supply With Demand Challenge](https://sqlperformance.com/2021/12/t-sql-queries/supply-demand-challenge)
- [Itzik Ben Gan Matching Supply With Demand Solutions Part 1](https://sqlperformance.com/2022/01/t-sql-queries/supply-demand-solutions-1)
- [LeetCode Tree Node](https://leetcode.com/problems/tree-node/)
- [SQLite Window Functions](https://sqlite.org/windowfunctions.html)

## Pattern map

| Pattern | Exercises |
| --- | --- |
| Unordered pairs and symmetry breaking | [Q01](QUESTIONS.md#q01-deduplicate-reverse-routes-while-preserving-an-original-row), [Q02](QUESTIONS.md#q02-find-reciprocal-pairs-without-matching-a-row-to-itself) |
| Graph edge normalization | [Q03](QUESTIONS.md#q03-count-undirected-neighbors-despite-duplicated-edge-directions), [Q04](QUESTIONS.md#q04-find-graph-triangles-exactly-once) |
| Recursive reachability | [Q05](QUESTIONS.md#q05-assign-connected-components-including-isolated-nodes), [Q46](QUESTIONS.md#q46-find-all-descendants-without-looping-on-cyclic-relationships) |
| Gaps and islands | [Q06](QUESTIONS.md#q06-compress-integer-sequences-with-duplicate-input-values), [Q07](QUESTIONS.md#q07-find-every-longest-login-streak-with-duplicate-logins), [Q08](QUESTIONS.md#q08-find-missing-ranges-including-the-boundaries), [Q11](QUESTIONS.md#q11-return-every-row-in-qualifying-id-streaks), [Q12](QUESTIONS.md#q12-reconstruct-projects-from-one-day-tasks), [Q41](QUESTIONS.md#q41-detect-repeated-values-by-row-adjacency-rather-than-id-arithmetic) |
| Sessionization and change points | [Q09](QUESTIONS.md#q09-sessionize-events-with-an-exact-inactivity-threshold), [Q10](QUESTIONS.md#q10-group-status-runs-with-null-states-and-missing-days) |
| Interval packing and sweep lines | [Q13](QUESTIONS.md#q13-merge-overlapping-intervals-even-when-they-are-nested), [Q14](QUESTIONS.md#q14-find-free-time-between-overlapping-bookings), [Q15](QUESTIONS.md#q15-find-peak-simultaneous-meetings-with-tied-event-times), [Q16](QUESTIONS.md#q16-measure-occupied-duration-without-counting-overlaps-twice) |
| Temporal and nearest joins | [Q17](QUESTIONS.md#q17-resolve-prices-as-of-a-date-while-keeping-products-without-history), [Q18](QUESTIONS.md#q18-join-facts-to-effective-dated-dimensions-at-a-shared-boundary), [Q19](QUESTIONS.md#q19-choose-the-closest-observation-with-a-deterministic-tie-rule) |
| NULL semantics and anti joins | [Q20](QUESTIONS.md#q20-find-nonbuyers-when-the-purchase-table-contains-null), [Q21](QUESTIONS.md#q21-keep-parents-that-have-no-qualifying-child-rows) |
| Join grain and multiplicity | [Q22](QUESTIONS.md#q22-aggregate-orders-and-payments-without-join-fan-out), [Q23](QUESTIONS.md#q23-preserve-independent-transaction-amounts-when-duplicate-values-are-valid) |
| Set and multiset reconciliation | [Q24](QUESTIONS.md#q24-reconcile-two-snapshots-including-null-valued-changes), [Q25](QUESTIONS.md#q25-reconcile-duplicate-counts-rather-than-just-distinct-rows) |
| Relational division and set equality | [Q26](QUESTIONS.md#q26-find-customers-covering-every-required-product), [Q27](QUESTIONS.md#q27-find-customers-whose-basket-exactly-equals-the-required-set), [Q28](QUESTIONS.md#q28-find-pairs-of-customers-with-identical-baskets-including-empty-ones) |
| Universal conditions and exclusion | [Q29](QUESTIONS.md#q29-find-students-who-never-scored-an-exam-extreme) |
| Independent grouping grains | [Q30](QUESTIONS.md#q30-combine-duplicate-and-unique-conditions-at-different-grains) |
| Window frames and peer rows | [Q31](QUESTIONS.md#q31-explain-peer-expansion-in-rows-versus-range), [Q32](QUESTIONS.md#q32-get-the-true-last-value-rather-than-the-last-value-so-far) |
| Window frames and missing values | [Q33](QUESTIONS.md#q33-forward-fill-nulls-even-when-values-decrease), [Q36](QUESTIONS.md#q36-maintain-a-cumulative-distinct-count-without-a-distinct-window-aggregate) |
| Calendar completion and rolling windows | [Q34](QUESTIONS.md#q34-compute-a-calendar-rolling-average-with-missing-days), [Q35](QUESTIONS.md#q35-count-distinct-active-users-across-a-rolling-calendar-window) |
| Order statistics and weighted distributions | [Q37](QUESTIONS.md#q37-compute-group-medians-without-losing-duplicate-observations), [Q38](QUESTIONS.md#q38-find-the-median-from-value-frequencies-without-expanding-rows) |
| Prefix constraints and cumulative state | [Q39](QUESTIONS.md#q39-find-the-last-person-in-a-capacity-limited-boarding-prefix), [Q40](QUESTIONS.md#q40-reset-running-totals-at-reset-events) |
| Positional pairing | [Q42](QUESTIONS.md#q42-swap-neighboring-seats-when-seat-ids-are-sparse) |
| Role unpivoting and tie rules | [Q43](QUESTIONS.md#q43-choose-tournament-winners-when-players-occupy-either-match-column) |
| Grain and denominator traps | [Q44](QUESTIONS.md#q44-compute-cohort-retention-with-a-fixed-signup-denominator) |
| Calendar adjacency and preaggregation | [Q45](QUESTIONS.md#q45-find-consecutive-over-limit-months-across-a-year-boundary) |
| Hierarchy classification | [Q47](QUESTIONS.md#q47-classify-tree-nodes-with-root-precedence) |
| Ordered event matching | [Q48](QUESTIONS.md#q48-find-ordered-funnel-completions-rather-than-mere-event-presence) |
| Cumulative interval matching and FIFO | [Q49](QUESTIONS.md#q49-allocate-supply-to-demand-in-fifo-order-without-a-cursor), [Q50](QUESTIONS.md#q50-value-remaining-fifo-inventory-with-a-partially-consumed-batch) |
