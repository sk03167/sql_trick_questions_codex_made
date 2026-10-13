# SQL Trick Questions and Sample Datasets

Practice 50 SQL puzzles where the main challenge is identifying a hidden assumption, preserving the correct data grain, or recognizing a reusable pattern. Basic counts and ordinary highest-salary ranking questions are excluded.

## How to practice

Use one exercise per fresh database. Each question has its own runnable CREATE TABLE and INSERT statements, sample tables, and expected output. Solutions are in [SOLUTIONS.md](SOLUTIONS.md). Numbering matches across both documents. Expected rows are ordered as shown. Difficulty labels are editorial estimates for these variants, not source-platform ratings.

The reference execution dialect is **SQLite 3.28 or newer**, available through Python standard library sqlite3. Every exercise also links to a PySpark DataFrame implementation with explicit input schemas. Most queries use broadly shared SQL constructs; dialect changes are listed in [SOLUTIONS.md](SOLUTIONS.md#dialect-and-data-conventions). Calendar days, elapsed minutes, and month ordinals are deliberately integers so the pattern is visible without engine-specific date syntax. Day ordinals are not YYYYMMDD values.

## Pattern index

| ID | Question | Pattern | Difficulty |
| --- | --- | --- | --- |
| Q01 | [Deduplicate reverse routes while preserving an original row](#q01-deduplicate-reverse-routes-while-preserving-an-original-row) | Unordered pairs and symmetry breaking | Medium |
| Q02 | [Find reciprocal pairs without matching a row to itself](#q02-find-reciprocal-pairs-without-matching-a-row-to-itself) | Unordered pairs and symmetry breaking | Medium |
| Q03 | [Count undirected neighbors despite duplicated edge directions](#q03-count-undirected-neighbors-despite-duplicated-edge-directions) | Graph edge normalization | Medium |
| Q04 | [Find graph triangles exactly once](#q04-find-graph-triangles-exactly-once) | Graph edge normalization | Hard |
| Q05 | [Assign connected components including isolated nodes](#q05-assign-connected-components-including-isolated-nodes) | Recursive reachability | Hard |
| Q06 | [Compress integer sequences with duplicate input values](#q06-compress-integer-sequences-with-duplicate-input-values) | Gaps and islands | Medium |
| Q07 | [Find every longest login streak with duplicate logins](#q07-find-every-longest-login-streak-with-duplicate-logins) | Gaps and islands | Medium |
| Q08 | [Find missing ranges including the boundaries](#q08-find-missing-ranges-including-the-boundaries) | Gaps and islands | Medium |
| Q09 | [Sessionize events with an exact inactivity threshold](#q09-sessionize-events-with-an-exact-inactivity-threshold) | Sessionization and change points | Medium |
| Q10 | [Group status runs with NULL states and missing days](#q10-group-status-runs-with-null-states-and-missing-days) | Sessionization and change points | Hard |
| Q11 | [Return every row in qualifying ID streaks](#q11-return-every-row-in-qualifying-id-streaks) | Gaps and islands | Medium |
| Q12 | [Reconstruct projects from one day tasks](#q12-reconstruct-projects-from-one-day-tasks) | Gaps and islands | Medium |
| Q13 | [Merge overlapping intervals even when they are nested](#q13-merge-overlapping-intervals-even-when-they-are-nested) | Interval packing and sweep lines | Hard |
| Q14 | [Find free time between overlapping bookings](#q14-find-free-time-between-overlapping-bookings) | Interval packing and sweep lines | Hard |
| Q15 | [Find peak simultaneous meetings with tied event times](#q15-find-peak-simultaneous-meetings-with-tied-event-times) | Interval packing and sweep lines | Hard |
| Q16 | [Measure occupied duration without counting overlaps twice](#q16-measure-occupied-duration-without-counting-overlaps-twice) | Interval packing and sweep lines | Hard |
| Q17 | [Resolve prices as of a date while keeping products without history](#q17-resolve-prices-as-of-a-date-while-keeping-products-without-history) | Temporal and nearest joins | Medium |
| Q18 | [Join facts to effective dated dimensions at a shared boundary](#q18-join-facts-to-effective-dated-dimensions-at-a-shared-boundary) | Temporal and nearest joins | Medium |
| Q19 | [Choose the closest observation with a deterministic tie rule](#q19-choose-the-closest-observation-with-a-deterministic-tie-rule) | Temporal and nearest joins | Hard |
| Q20 | [Find nonbuyers when the purchase table contains NULL](#q20-find-nonbuyers-when-the-purchase-table-contains-null) | NULL semantics and anti joins | Medium |
| Q21 | [Keep parents that have no qualifying child rows](#q21-keep-parents-that-have-no-qualifying-child-rows) | NULL semantics and anti joins | Medium |
| Q22 | [Aggregate orders and payments without join fan out](#q22-aggregate-orders-and-payments-without-join-fan-out) | Join grain and multiplicity | Hard |
| Q23 | [Preserve independent transaction amounts when duplicate values are valid](#q23-preserve-independent-transaction-amounts-when-duplicate-values-are-valid) | Join grain and multiplicity | Medium |
| Q24 | [Reconcile two snapshots including NULL valued changes](#q24-reconcile-two-snapshots-including-null-valued-changes) | Set and multiset reconciliation | Hard |
| Q25 | [Reconcile duplicate counts rather than just distinct rows](#q25-reconcile-duplicate-counts-rather-than-just-distinct-rows) | Set and multiset reconciliation | Hard |
| Q26 | [Find customers covering every required product](#q26-find-customers-covering-every-required-product) | Relational division and set equality | Hard |
| Q27 | [Find customers whose basket exactly equals the required set](#q27-find-customers-whose-basket-exactly-equals-the-required-set) | Relational division and set equality | Hard |
| Q28 | [Find pairs of customers with identical baskets including empty ones](#q28-find-pairs-of-customers-with-identical-baskets-including-empty-ones) | Relational division and set equality | Hard |
| Q29 | [Find students who never scored an exam extreme](#q29-find-students-who-never-scored-an-exam-extreme) | Universal conditions and exclusion | Hard |
| Q30 | [Combine duplicate and unique conditions at different grains](#q30-combine-duplicate-and-unique-conditions-at-different-grains) | Independent grouping grains | Hard |
| Q31 | [Explain peer expansion in ROWS versus RANGE](#q31-explain-peer-expansion-in-rows-versus-range) | Window frames and peer rows | Medium |
| Q32 | [Get the true last value rather than the last value so far](#q32-get-the-true-last-value-rather-than-the-last-value-so-far) | Window frames and peer rows | Medium |
| Q33 | [Forward fill NULLs even when values decrease](#q33-forward-fill-nulls-even-when-values-decrease) | Window frames and missing values | Hard |
| Q34 | [Compute a calendar rolling average with missing days](#q34-compute-a-calendar-rolling-average-with-missing-days) | Calendar completion and rolling windows | Hard |
| Q35 | [Count distinct active users across a rolling calendar window](#q35-count-distinct-active-users-across-a-rolling-calendar-window) | Calendar completion and rolling windows | Hard |
| Q36 | [Maintain a cumulative distinct count without a distinct window aggregate](#q36-maintain-a-cumulative-distinct-count-without-a-distinct-window-aggregate) | Window frames and missing values | Hard |
| Q37 | [Compute group medians without losing duplicate observations](#q37-compute-group-medians-without-losing-duplicate-observations) | Order statistics and weighted distributions | Hard |
| Q38 | [Find the median from value frequencies without expanding rows](#q38-find-the-median-from-value-frequencies-without-expanding-rows) | Order statistics and weighted distributions | Hard |
| Q39 | [Find the last person in a capacity limited boarding prefix](#q39-find-the-last-person-in-a-capacity-limited-boarding-prefix) | Prefix constraints and cumulative state | Medium |
| Q40 | [Reset running totals at reset events](#q40-reset-running-totals-at-reset-events) | Prefix constraints and cumulative state | Hard |
| Q41 | [Detect repeated values by row adjacency rather than ID arithmetic](#q41-detect-repeated-values-by-row-adjacency-rather-than-id-arithmetic) | Gaps and islands | Medium |
| Q42 | [Swap neighboring seats when seat IDs are sparse](#q42-swap-neighboring-seats-when-seat-ids-are-sparse) | Positional pairing | Hard |
| Q43 | [Choose tournament winners when players occupy either match column](#q43-choose-tournament-winners-when-players-occupy-either-match-column) | Role unpivoting and tie rules | Hard |
| Q44 | [Compute cohort retention with a fixed signup denominator](#q44-compute-cohort-retention-with-a-fixed-signup-denominator) | Grain and denominator traps | Hard |
| Q45 | [Find consecutive over limit months across a year boundary](#q45-find-consecutive-over-limit-months-across-a-year-boundary) | Calendar adjacency and preaggregation | Hard |
| Q46 | [Find all descendants without looping on cyclic relationships](#q46-find-all-descendants-without-looping-on-cyclic-relationships) | Recursive reachability | Hard |
| Q47 | [Classify tree nodes with root precedence](#q47-classify-tree-nodes-with-root-precedence) | Hierarchy classification | Medium |
| Q48 | [Find ordered funnel completions rather than mere event presence](#q48-find-ordered-funnel-completions-rather-than-mere-event-presence) | Ordered event matching | Hard |
| Q49 | [Allocate supply to demand in FIFO order without a cursor](#q49-allocate-supply-to-demand-in-fifo-order-without-a-cursor) | Cumulative interval matching and FIFO | Hard |
| Q50 | [Value remaining FIFO inventory with a partially consumed batch](#q50-value-remaining-fifo-inventory-with-a-partially-consumed-batch) | Cumulative interval matching and FIFO | Hard |

## Q01 Deduplicate reverse routes while preserving an original row

**Pattern:** Unordered pairs and symmetry breaking

**Difficulty:** Medium

Original extension of a symmetric pair pattern. Pattern reference: [HackerRank Symmetric Pairs](https://www.hackerrank.com/challenges/symmetric-pairs/problem).

Treat (source, destination, distance) and its reversal as one route. Preserve the smallest row_id in each duplicate group, including exact duplicates. Different distances are different routes; keep self routes and lone reverse-oriented routes. Endpoints and distance are non-null.

### Sample data

**routes**

| row_id | src | dst | dist |
| --- | --- | --- | --- |
| 1 | A | B | 10 |
| 2 | B | A | 10 |
| 3 | A | C | 5 |
| 4 | D | C | 7 |
| 5 | A | B | 10 |
| 6 | A | A | 0 |
| 7 | B | A | 12 |

### SQL setup

```sql
CREATE TABLE routes (
    row_id INTEGER PRIMARY KEY,
    src TEXT,
    dst TEXT,
    dist INTEGER
);

INSERT INTO routes (row_id, src, dst, dist) VALUES
    (1, 'A', 'B', 10),
    (2, 'B', 'A', 10),
    (3, 'A', 'C', 5),
    (4, 'D', 'C', 7),
    (5, 'A', 'B', 10),
    (6, 'A', 'A', 0),
    (7, 'B', 'A', 12);
```

### Expected output

| row_id | src | dst | dist |
| --- | --- | --- | --- |
| 1 | A | B | 10 |
| 3 | A | C | 5 |
| 4 | D | C | 7 |
| 6 | A | A | 0 |
| 7 | B | A | 12 |

[SQL solution](SOLUTIONS.md#q01-deduplicate-reverse-routes-while-preserving-an-original-row) · [PySpark solution](SOLUTIONS.md#pyspark-q01)

## Q02 Find reciprocal pairs without matching a row to itself

**Pattern:** Unordered pairs and symmetry breaking

**Difficulty:** Medium

Adapted practice problem with fresh data. Source pattern: [HackerRank Symmetric Pairs](https://www.hackerrank.com/challenges/symmetric-pairs/problem).

Return (x,y) with x <= y when two distinct input rows establish both directions. A self pair (x,x) needs at least two physical rows. Return each pair once.

### Sample data

**pairs**

| id | x | y |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 1 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 4 | 4 |
| 6 | 5 | 6 |
| 7 | 1 | 2 |

### SQL setup

```sql
CREATE TABLE pairs (
    id INTEGER PRIMARY KEY,
    x INTEGER,
    y INTEGER
);

INSERT INTO pairs (id, x, y) VALUES
    (1, 1, 2),
    (2, 2, 1),
    (3, 3, 3),
    (4, 4, 4),
    (5, 4, 4),
    (6, 5, 6),
    (7, 1, 2);
```

### Expected output

| x | y |
| --- | --- |
| 1 | 2 |
| 4 | 4 |

[SQL solution](SOLUTIONS.md#q02-find-reciprocal-pairs-without-matching-a-row-to-itself) · [PySpark solution](SOLUTIONS.md#pyspark-q02)

## Q03 Count undirected neighbors despite duplicated edge directions

**Pattern:** Graph edge normalization

**Difficulty:** Medium

Original extension of a published bidirectional friendship problem. Pattern reference: [LeetCode Friend Requests II](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/).

Return each registered person and the number of distinct other people connected to them. Edges are undirected; duplicate directions and self edges must not inflate counts. Include isolated people.

### Sample data

**people**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |

**edges**

| a | b |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 3 |

### SQL setup

```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY
);

INSERT INTO people (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE edges (
    a INTEGER,
    b INTEGER
);

INSERT INTO edges (a, b) VALUES
    (1, 2),
    (2, 1),
    (1, 2),
    (2, 3),
    (3, 3);
```

### Expected output

| id | neighbors |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

[SQL solution](SOLUTIONS.md#q03-count-undirected-neighbors-despite-duplicated-edge-directions) · [PySpark solution](SOLUTIONS.md#pyspark-q03)

## Q04 Find graph triangles exactly once

**Pattern:** Graph edge normalization

**Difficulty:** Hard

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

Return all undirected triangles as a < b < c. Ignore duplicate edges and self edges. A triangle requires all three edges, not just a two-hop path.

### Sample data

**edges**

| src | dst |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 2 | 3 |
| 1 | 3 |
| 1 | 4 |
| 3 | 4 |
| 4 | 4 |

### SQL setup

```sql
CREATE TABLE edges (
    src INTEGER,
    dst INTEGER
);

INSERT INTO edges (src, dst) VALUES
    (1, 2),
    (2, 1),
    (2, 3),
    (1, 3),
    (1, 4),
    (3, 4),
    (4, 4);
```

### Expected output

| a | b | c |
| --- | --- | --- |
| 1 | 2 | 3 |
| 1 | 3 | 4 |

[SQL solution](SOLUTIONS.md#q04-find-graph-triangles-exactly-once) · [PySpark solution](SOLUTIONS.md#pyspark-q04)

## Q05 Assign connected components including isolated nodes

**Pattern:** Recursive reachability

**Difficulty:** Hard

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

Return each node with the smallest node ID in its undirected connected component. Include isolated nodes. Edges can contain cycles and duplicates.

### Sample data

**nodes**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |

**edges**

| a | b |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 1 |
| 4 | 5 |
| 1 | 2 |

### SQL setup

```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY
);

INSERT INTO nodes (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5),
    (6);

CREATE TABLE edges (
    a INTEGER,
    b INTEGER
);

INSERT INTO edges (a, b) VALUES
    (1, 2),
    (2, 3),
    (3, 1),
    (4, 5),
    (1, 2);
```

### Expected output

| node | component |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 4 |
| 5 | 4 |
| 6 | 6 |

[SQL solution](SOLUTIONS.md#q05-assign-connected-components-including-isolated-nodes) · [PySpark solution](SOLUTIONS.md#pyspark-q05)

## Q06 Compress integer sequences with duplicate input values

**Pattern:** Gaps and islands

**Difficulty:** Medium

Original practice extension of contiguous grouping. Pattern reference: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

Return start_value, end_value, and distinct length for every maximal consecutive integer run. Duplicate observations count once.

### Sample data

**observations**

| value |
| --- |
| 1 |
| 2 |
| 2 |
| 3 |
| 7 |
| 8 |
| 10 |

### SQL setup

```sql
CREATE TABLE observations (
    value INTEGER
);

INSERT INTO observations (value) VALUES
    (1),
    (2),
    (2),
    (3),
    (7),
    (8),
    (10);
```

### Expected output

| start_value | end_value | length |
| --- | --- | --- |
| 1 | 3 | 3 |
| 7 | 8 | 2 |
| 10 | 10 | 1 |

[SQL solution](SOLUTIONS.md#q06-compress-integer-sequences-with-duplicate-input-values) · [PySpark solution](SOLUTIONS.md#pyspark-q06)

## Q07 Find every longest login streak with duplicate logins

**Pattern:** Gaps and islands

**Difficulty:** Medium

Original practice extension. Pattern reference: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

day_no is a calendar-day ordinal, not a YYYYMMDD integer. Return all longest streaks per user, including ties. Multiple logins on the same day count once.

### Sample data

**logins**

| user_id | day_no |
| --- | --- |
| 1 | 1 |
| 1 | 2 |
| 1 | 2 |
| 1 | 4 |
| 1 | 5 |
| 2 | 2 |
| 2 | 3 |
| 2 | 4 |

### SQL setup

```sql
CREATE TABLE logins (
    user_id INTEGER,
    day_no INTEGER
);

INSERT INTO logins (user_id, day_no) VALUES
    (1, 1),
    (1, 2),
    (1, 2),
    (1, 4),
    (1, 5),
    (2, 2),
    (2, 3),
    (2, 4);
```

### Expected output

| user_id | start_day | end_day | days |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 2 |
| 1 | 4 | 5 | 2 |
| 2 | 2 | 4 | 3 |

[SQL solution](SOLUTIONS.md#q07-find-every-longest-login-streak-with-duplicate-logins) · [PySpark solution](SOLUTIONS.md#pyspark-q07)

## Q08 Find missing ranges including the boundaries

**Pattern:** Gaps and islands

**Difficulty:** Medium

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

Find all missing inclusive integer ranges within 1 through 12. Existing IDs are distinct and within the bounds. Include leading and trailing gaps without returning each missing ID separately.

### Sample data

**ids**

| id |
| --- |
| 3 |
| 4 |
| 8 |
| 10 |

### SQL setup

```sql
CREATE TABLE ids (
    id INTEGER PRIMARY KEY
);

INSERT INTO ids (id) VALUES
    (3),
    (4),
    (8),
    (10);
```

### Expected output

| gap_start | gap_end |
| --- | --- |
| 1 | 2 |
| 5 | 7 |
| 9 | 9 |
| 11 | 12 |

[SQL solution](SOLUTIONS.md#q08-find-missing-ranges-including-the-boundaries) · [PySpark solution](SOLUTIONS.md#pyspark-q08)

## Q09 Sessionize events with an exact inactivity threshold

**Pattern:** Sessionization and change points

**Difficulty:** Medium

Adapted pattern with fresh data and explicit boundary semantics. Source pattern: [Ryan Guill Aggregating event data into sessions](https://ryanguill.com/postgresql/sql/2024/06/24/aggregating-event-data-into-sessions.html).

minute_no is an elapsed-minute ordinal. Start a new session only when the gap from the previous event is greater than 30 minutes. Equal timestamps are ordered by event_id. Return user, session number, start minute, end minute, and event count.

### Sample data

**events**

| event_id | user_id | minute_no |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 1 | 30 |
| 3 | 1 | 61 |
| 4 | 1 | 61 |
| 5 | 2 | 5 |
| 6 | 2 | 40 |

### SQL setup

```sql
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    minute_no INTEGER
);

INSERT INTO events (event_id, user_id, minute_no) VALUES
    (1, 1, 0),
    (2, 1, 30),
    (3, 1, 61),
    (4, 1, 61),
    (5, 2, 5),
    (6, 2, 40);
```

### Expected output

| user_id | session_no | start_minute | end_minute | events |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 30 | 2 |
| 1 | 2 | 61 | 61 | 2 |
| 2 | 1 | 5 | 5 | 1 |
| 2 | 2 | 40 | 40 | 1 |

[SQL solution](SOLUTIONS.md#q09-sessionize-events-with-an-exact-inactivity-threshold) · [PySpark solution](SOLUTIONS.md#pyspark-q09)

## Q10 Group status runs with NULL states and missing days

**Pattern:** Sessionization and change points

**Difficulty:** Hard

Original practice extension. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Return maximal runs of the same status on consecutive calendar-day ordinals. NULL is a legitimate status and equals another NULL for grouping. A missing day breaks a run even if status stays the same. One row exists per day.

### Sample data

**daily**

| day_no | status |
| --- | --- |
| 1 | up |
| 2 | up |
| 3 | NULL |
| 4 | NULL |
| 6 | NULL |
| 7 | up |

### SQL setup

```sql
CREATE TABLE daily (
    day_no INTEGER PRIMARY KEY,
    status TEXT
);

INSERT INTO daily (day_no, status) VALUES
    (1, 'up'),
    (2, 'up'),
    (3, NULL),
    (4, NULL),
    (6, NULL),
    (7, 'up');
```

### Expected output

| status | start_day | end_day |
| --- | --- | --- |
| up | 1 | 2 |
| NULL | 3 | 4 |
| NULL | 6 | 6 |
| up | 7 | 7 |

[SQL solution](SOLUTIONS.md#q10-group-status-runs-with-null-states-and-missing-days) · [PySpark solution](SOLUTIONS.md#pyspark-q10)

## Q11 Return every row in qualifying ID streaks

**Pattern:** Gaps and islands

**Difficulty:** Medium

Adapted problem with fresh data. Source pattern: [LeetCode Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/).

Return all rows belonging to at least three consecutive IDs whose attendance is at least 100. Adjacency is by ID, not by calendar date. IDs are unique.

### Sample data

**visits**

| id | day_no | people |
| --- | --- | --- |
| 1 | 1 | 90 |
| 2 | 2 | 110 |
| 3 | 3 | 120 |
| 4 | 4 | 90 |
| 5 | 5 | 130 |
| 6 | 6 | 140 |
| 7 | 9 | 150 |
| 9 | 10 | 160 |

### SQL setup

```sql
CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    day_no INTEGER,
    people INTEGER
);

INSERT INTO visits (id, day_no, people) VALUES
    (1, 1, 90),
    (2, 2, 110),
    (3, 3, 120),
    (4, 4, 90),
    (5, 5, 130),
    (6, 6, 140),
    (7, 9, 150),
    (9, 10, 160);
```

### Expected output

| id | day_no | people |
| --- | --- | --- |
| 5 | 5 | 130 |
| 6 | 6 | 140 |
| 7 | 9 | 150 |

[SQL solution](SOLUTIONS.md#q11-return-every-row-in-qualifying-id-streaks) · [PySpark solution](SOLUTIONS.md#pyspark-q11)

## Q12 Reconstruct projects from one day tasks

**Pattern:** Gaps and islands

**Difficulty:** Medium

Adapted problem with fresh data. Source pattern: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

Each task covers [start_day,end_day) and lasts exactly one day. Tasks do not overlap. Adjacent tasks belong to one project. Return project start, end, and duration, ordered by duration then start.

### Sample data

**tasks**

| id | start_day | end_day |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 3 |
| 3 | 5 | 6 |
| 4 | 8 | 9 |
| 5 | 9 | 10 |
| 6 | 10 | 11 |

### SQL setup

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    start_day INTEGER,
    end_day INTEGER
);

INSERT INTO tasks (id, start_day, end_day) VALUES
    (1, 1, 2),
    (2, 2, 3),
    (3, 5, 6),
    (4, 8, 9),
    (5, 9, 10),
    (6, 10, 11);
```

### Expected output

| project_start | project_end | duration |
| --- | --- | --- |
| 5 | 6 | 1 |
| 1 | 3 | 2 |
| 8 | 11 | 3 |

[SQL solution](SOLUTIONS.md#q12-reconstruct-projects-from-one-day-tasks) · [PySpark solution](SOLUTIONS.md#pyspark-q12)

## Q13 Merge overlapping intervals even when they are nested

**Pattern:** Interval packing and sweep lines

**Difficulty:** Hard

Adapted pattern with a nested-interval counterexample. Source pattern: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

Merge intervals into maximal coverage ranges. Intervals use [start,end); touching intervals merge. Input intervals have positive lengths and unique IDs. Include nested ranges correctly.

### Sample data

**intervals**

| id | start_at | end_at |
| --- | --- | --- |
| 1 | 1 | 10 |
| 2 | 2 | 3 |
| 3 | 4 | 8 |
| 4 | 10 | 12 |
| 5 | 15 | 17 |

### SQL setup

```sql
CREATE TABLE intervals (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO intervals (id, start_at, end_at) VALUES
    (1, 1, 10),
    (2, 2, 3),
    (3, 4, 8),
    (4, 10, 12),
    (5, 15, 17);
```

### Expected output

| start_at | end_at |
| --- | --- |
| 1 | 12 |
| 15 | 17 |

[SQL solution](SOLUTIONS.md#q13-merge-overlapping-intervals-even-when-they-are-nested) · [PySpark solution](SOLUTIONS.md#pyspark-q13)

## Q14 Find free time between overlapping bookings

**Pattern:** Interval packing and sweep lines

**Difficulty:** Hard

Original practice extension. Pattern reference: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

Within [0,20), return every maximal free interval. Bookings are positive-length half-open intervals fully inside the requested window. Touching occupied intervals leave no gap.

### Sample data

**bookings**

| id | start_at | end_at |
| --- | --- | --- |
| 1 | 1 | 5 |
| 2 | 3 | 7 |
| 3 | 10 | 12 |
| 4 | 12 | 16 |

### SQL setup

```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO bookings (id, start_at, end_at) VALUES
    (1, 1, 5),
    (2, 3, 7),
    (3, 10, 12),
    (4, 12, 16);
```

### Expected output

| free_start | free_end |
| --- | --- |
| 0 | 1 |
| 7 | 10 |
| 16 | 20 |

[SQL solution](SOLUTIONS.md#q14-find-free-time-between-overlapping-bookings) · [PySpark solution](SOLUTIONS.md#pyspark-q14)

## Q15 Find peak simultaneous meetings with tied event times

**Pattern:** Interval packing and sweep lines

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Meetings are half-open intervals: a meeting ending at time t is inactive at t. Return every positive-duration segment having the maximum simultaneous meeting count.

### Sample data

**meetings**

| id | start_at | end_at |
| --- | --- | --- |
| 1 | 1 | 4 |
| 2 | 2 | 5 |
| 3 | 4 | 6 |
| 4 | 4 | 7 |

### SQL setup

```sql
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    start_at INTEGER,
    end_at INTEGER
);

INSERT INTO meetings (id, start_at, end_at) VALUES
    (1, 1, 4),
    (2, 2, 5),
    (3, 4, 6),
    (4, 4, 7);
```

### Expected output

| start_at | end_at | active |
| --- | --- | --- |
| 4 | 5 | 3 |

[SQL solution](SOLUTIONS.md#q15-find-peak-simultaneous-meetings-with-tied-event-times) · [PySpark solution](SOLUTIONS.md#pyspark-q15)

## Q16 Measure occupied duration without counting overlaps twice

**Pattern:** Interval packing and sweep lines

**Difficulty:** Hard

Original practice extension. Pattern reference: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

Return total occupied duration across half-open intervals. Duplicate and nested coverage must count once. Touching ranges may be merged.

### Sample data

**ranges**

| id | s | e |
| --- | --- | --- |
| 1 | 1 | 10 |
| 2 | 2 | 3 |
| 3 | 9 | 12 |
| 4 | 15 | 18 |

### SQL setup

```sql
CREATE TABLE ranges (
    id INTEGER PRIMARY KEY,
    s INTEGER,
    e INTEGER
);

INSERT INTO ranges (id, s, e) VALUES
    (1, 1, 10),
    (2, 2, 3),
    (3, 9, 12),
    (4, 15, 18);
```

### Expected output

| occupied |
| --- |
| 14 |

[SQL solution](SOLUTIONS.md#q16-measure-occupied-duration-without-counting-overlaps-twice) · [PySpark solution](SOLUTIONS.md#pyspark-q16)

## Q17 Resolve prices as of a date while keeping products without history

**Pattern:** Temporal and nearest joins

**Difficulty:** Medium

Adapted pattern with fresh data and a product master. Source pattern: [LeetCode Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/).

Return every product price at day_no 5. Use the most recent change at or before that day; otherwise use default price 10. Product IDs come from a master table, so products with no history must appear. Changes are unique by product and day.

### Sample data

**products**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |

**changes**

| product_id | day_no | price |
| --- | --- | --- |
| 1 | 2 | 20 |
| 1 | 5 | 30 |
| 1 | 8 | 99 |
| 2 | 7 | 40 |
| 3 | 3 | 15 |

### SQL setup

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY
);

INSERT INTO products (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE changes (
    product_id INTEGER,
    day_no INTEGER,
    price INTEGER
);

INSERT INTO changes (product_id, day_no, price) VALUES
    (1, 2, 20),
    (1, 5, 30),
    (1, 8, 99),
    (2, 7, 40),
    (3, 3, 15);
```

### Expected output

| id | price |
| --- | --- |
| 1 | 30 |
| 2 | 10 |
| 3 | 15 |
| 4 | 10 |

[SQL solution](SOLUTIONS.md#q17-resolve-prices-as-of-a-date-while-keeping-products-without-history) · [PySpark solution](SOLUTIONS.md#pyspark-q17)

## Q18 Join facts to effective dated dimensions at a shared boundary

**Pattern:** Temporal and nearest joins

**Difficulty:** Medium

Original practice exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

Attach the effective label to each fact using [valid_from,valid_to). NULL valid_to means open-ended. Return NULL for uncovered facts. Dimension periods for each key never overlap.

### Sample data

**facts**

| id | key_id | at |
| --- | --- | --- |
| 1 | 1 | 4 |
| 2 | 1 | 5 |
| 3 | 1 | 10 |
| 4 | 2 | 5 |

**versions**

| key_id | valid_from | valid_to | label |
| --- | --- | --- | --- |
| 1 | 1 | 5 | old |
| 1 | 5 | 10 | new |
| 1 | 10 | NULL | latest |

### SQL setup

```sql
CREATE TABLE facts (
    id INTEGER PRIMARY KEY,
    key_id INTEGER,
    at INTEGER
);

INSERT INTO facts (id, key_id, at) VALUES
    (1, 1, 4),
    (2, 1, 5),
    (3, 1, 10),
    (4, 2, 5);

CREATE TABLE versions (
    key_id INTEGER,
    valid_from INTEGER,
    valid_to INTEGER,
    label TEXT
);

INSERT INTO versions (key_id, valid_from, valid_to, label) VALUES
    (1, 1, 5, 'old'),
    (1, 5, 10, 'new'),
    (1, 10, NULL, 'latest');
```

### Expected output

| id | label |
| --- | --- |
| 1 | old |
| 2 | new |
| 3 | latest |
| 4 | NULL |

[SQL solution](SOLUTIONS.md#q18-join-facts-to-effective-dated-dimensions-at-a-shared-boundary) · [PySpark solution](SOLUTIONS.md#pyspark-q18)

## Q19 Choose the closest observation with a deterministic tie rule

**Pattern:** Temporal and nearest joins

**Difficulty:** Hard

Adapted pattern with fresh data. Source pattern: [Itzik Ben Gan Closest Match Part 1](https://sqlperformance.com/2018/12/t-sql-queries/closest-match-part-1).

For each target minute, choose the nearest reading. A distance tie prefers the earlier reading minute, then the smaller reading ID. There is at least one reading; reading timestamps may duplicate.

### Sample data

**targets**

| id | at |
| --- | --- |
| 1 | 5 |
| 2 | 10 |
| 3 | 0 |

**readings**

| id | at | value |
| --- | --- | --- |
| 1 | 3 | 30 |
| 2 | 7 | 70 |
| 3 | 7 | 71 |
| 4 | 12 | 120 |

### SQL setup

```sql
CREATE TABLE targets (
    id INTEGER PRIMARY KEY,
    at INTEGER
);

INSERT INTO targets (id, at) VALUES
    (1, 5),
    (2, 10),
    (3, 0);

CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    value INTEGER
);

INSERT INTO readings (id, at, value) VALUES
    (1, 3, 30),
    (2, 7, 70),
    (3, 7, 71),
    (4, 12, 120);
```

### Expected output

| target_id | reading_id | value |
| --- | --- | --- |
| 1 | 1 | 30 |
| 2 | 4 | 120 |
| 3 | 1 | 30 |

[SQL solution](SOLUTIONS.md#q19-choose-the-closest-observation-with-a-deterministic-tie-rule) · [PySpark solution](SOLUTIONS.md#pyspark-q19)

## Q20 Find nonbuyers when the purchase table contains NULL

**Pattern:** NULL semantics and anti joins

**Difficulty:** Medium

Original semantics exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

Return registered customer IDs with no matching purchase. A purchase can have an unknown customer_id represented by NULL; it does not match any registered customer.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |
| 3 |

**purchases**

| id | customer_id |
| --- | --- |
| 1 | 1 |
| 2 | NULL |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3);

CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER
);

INSERT INTO purchases (id, customer_id) VALUES
    (1, 1),
    (2, NULL);
```

### Expected output

| id |
| --- |
| 2 |
| 3 |

[SQL solution](SOLUTIONS.md#q20-find-nonbuyers-when-the-purchase-table-contains-null) · [PySpark solution](SOLUTIONS.md#pyspark-q20)

## Q21 Keep parents that have no qualifying child rows

**Pattern:** NULL semantics and anti joins

**Difficulty:** Medium

Original semantics exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

Return every customer with the number of paid orders. Customers with only cancelled orders, or no orders, must have zero.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |
| 3 |

**orders**

| id | customer_id | status |
| --- | --- | --- |
| 11 | 1 | paid |
| 12 | 1 | cancelled |
| 13 | 2 | cancelled |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    status TEXT
);

INSERT INTO orders (id, customer_id, status) VALUES
    (11, 1, 'paid'),
    (12, 1, 'cancelled'),
    (13, 2, 'cancelled');
```

### Expected output

| id | paid_orders |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |

[SQL solution](SOLUTIONS.md#q21-keep-parents-that-have-no-qualifying-child-rows) · [PySpark solution](SOLUTIONS.md#pyspark-q21)

## Q22 Aggregate orders and payments without join fan out

**Pattern:** Join grain and multiplicity

**Difficulty:** Hard

Original practice exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

Return every customer, total order amount, and total payment amount. Orders and payments are separate one-to-many children of customers. A customer can have no child rows. Amounts are non-null.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |

**orders**

| id | customer_id | amount |
| --- | --- | --- |
| 1 | 1 | 50 |
| 2 | 1 | 50 |

**payments**

| id | customer_id | amount |
| --- | --- | --- |
| 1 | 1 | 30 |
| 2 | 1 | 30 |
| 3 | 1 | 40 |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER
);

INSERT INTO orders (id, customer_id, amount) VALUES
    (1, 1, 50),
    (2, 1, 50);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER
);

INSERT INTO payments (id, customer_id, amount) VALUES
    (1, 1, 30),
    (2, 1, 30),
    (3, 1, 40);
```

### Expected output

| id | ordered | paid |
| --- | --- | --- |
| 1 | 100 | 100 |
| 2 | 0 | 0 |

[SQL solution](SOLUTIONS.md#q22-aggregate-orders-and-payments-without-join-fan-out) · [PySpark solution](SOLUTIONS.md#pyspark-q22)

## Q23 Preserve independent transaction amounts when duplicate values are valid

**Pattern:** Join grain and multiplicity

**Difficulty:** Medium

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

Sum the amount of invoices having at least one approved tag. Each invoice contributes once, even if multiple approved tags exist. Equal amounts on different invoices are legitimate.

### Sample data

**invoices**

| id | amount |
| --- | --- |
| 1 | 50 |
| 2 | 50 |
| 3 | 100 |

**tags**

| invoice_id | tag |
| --- | --- |
| 1 | approved |
| 1 | approved |
| 2 | approved |
| 3 | draft |

### SQL setup

```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    amount INTEGER
);

INSERT INTO invoices (id, amount) VALUES
    (1, 50),
    (2, 50),
    (3, 100);

CREATE TABLE tags (
    invoice_id INTEGER,
    tag TEXT
);

INSERT INTO tags (invoice_id, tag) VALUES
    (1, 'approved'),
    (1, 'approved'),
    (2, 'approved'),
    (3, 'draft');
```

### Expected output

| approved_total |
| --- |
| 100 |

[SQL solution](SOLUTIONS.md#q23-preserve-independent-transaction-amounts-when-duplicate-values-are-valid) · [PySpark solution](SOLUTIONS.md#pyspark-q23)

## Q24 Reconcile two snapshots including NULL valued changes

**Pattern:** Set and multiset reconciliation

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite SQL Expressions](https://www.sqlite.org/lang_expr.html).

Both snapshots have a unique non-null ID. Return added, removed, or changed IDs. NULL to value and value to NULL are changes; NULL to NULL is unchanged. Output id, change_kind, old_value, new_value.

### Sample data

**old_snapshot**

| id | val |
| --- | --- |
| 1 | a |
| 2 | NULL |
| 3 | c |
| 5 | NULL |

**new_snapshot**

| id | val |
| --- | --- |
| 1 | a |
| 2 | b |
| 4 | d |
| 5 | NULL |

### SQL setup

```sql
CREATE TABLE old_snapshot (
    id INTEGER PRIMARY KEY,
    val TEXT
);

INSERT INTO old_snapshot (id, val) VALUES
    (1, 'a'),
    (2, NULL),
    (3, 'c'),
    (5, NULL);

CREATE TABLE new_snapshot (
    id INTEGER PRIMARY KEY,
    val TEXT
);

INSERT INTO new_snapshot (id, val) VALUES
    (1, 'a'),
    (2, 'b'),
    (4, 'd'),
    (5, NULL);
```

### Expected output

| id | change_kind | old_value | new_value |
| --- | --- | --- | --- |
| 2 | changed | NULL | b |
| 3 | removed | c | NULL |
| 4 | added | NULL | d |

[SQL solution](SOLUTIONS.md#q24-reconcile-two-snapshots-including-null-valued-changes) · [PySpark solution](SOLUTIONS.md#pyspark-q24)

## Q25 Reconcile duplicate counts rather than just distinct rows

**Pattern:** Set and multiset reconciliation

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

Return keys whose multiplicity differs between two bags, with delta = new_count - old_count. NULL is a valid key. Suppress zero deltas.

### Sample data

**old_bag**

| key_name |
| --- |
| a |
| a |
| b |
| NULL |

**new_bag**

| key_name |
| --- |
| a |
| b |
| b |
| c |
| NULL |
| NULL |

### SQL setup

```sql
CREATE TABLE old_bag (
    key_name TEXT
);

INSERT INTO old_bag (key_name) VALUES
    ('a'),
    ('a'),
    ('b'),
    (NULL);

CREATE TABLE new_bag (
    key_name TEXT
);

INSERT INTO new_bag (key_name) VALUES
    ('a'),
    ('b'),
    ('b'),
    ('c'),
    (NULL),
    (NULL);
```

### Expected output

| key_name | delta |
| --- | --- |
| NULL | 1 |
| a | -1 |
| b | 1 |
| c | 1 |

[SQL solution](SOLUTIONS.md#q25-reconcile-duplicate-counts-rather-than-just-distinct-rows) · [PySpark solution](SOLUTIONS.md#pyspark-q25)

## Q26 Find customers covering every required product

**Pattern:** Relational division and set equality

**Difficulty:** Hard

Adapted pattern with duplicates, extras, and a master table. Source pattern: [LeetCode Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/).

Return registered customers who bought every required product. Extra purchases are allowed; repeated purchases do not help. When the required set is empty, every registered customer qualifies.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |

**required**

| product |
| --- |
| A |
| B |

**purchases**

| customer_id | product |
| --- | --- |
| 1 | A |
| 1 | A |
| 1 | B |
| 1 | X |
| 2 | A |
| 2 | A |
| 3 | A |
| 3 | B |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE required (
    product TEXT PRIMARY KEY
);

INSERT INTO required (product) VALUES
    ('A'),
    ('B');

CREATE TABLE purchases (
    customer_id INTEGER,
    product TEXT
);

INSERT INTO purchases (customer_id, product) VALUES
    (1, 'A'),
    (1, 'A'),
    (1, 'B'),
    (1, 'X'),
    (2, 'A'),
    (2, 'A'),
    (3, 'A'),
    (3, 'B');
```

### Expected output

| id |
| --- |
| 1 |
| 3 |

[SQL solution](SOLUTIONS.md#q26-find-customers-covering-every-required-product) · [PySpark solution](SOLUTIONS.md#pyspark-q26)

## Q27 Find customers whose basket exactly equals the required set

**Pattern:** Relational division and set equality

**Difficulty:** Hard

Original extension from containment to equality. Pattern reference: [LeetCode Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/).

Return customers whose distinct purchased products equal the required set: no missing product and no extra product. Products and customer IDs are non-null. Duplicate purchases are irrelevant.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |

**required**

| product |
| --- |
| A |
| B |

**purchases**

| customer_id | product |
| --- | --- |
| 1 | A |
| 1 | B |
| 1 | X |
| 2 | A |
| 3 | A |
| 3 | A |
| 3 | B |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE required (
    product TEXT PRIMARY KEY
);

INSERT INTO required (product) VALUES
    ('A'),
    ('B');

CREATE TABLE purchases (
    customer_id INTEGER,
    product TEXT
);

INSERT INTO purchases (customer_id, product) VALUES
    (1, 'A'),
    (1, 'B'),
    (1, 'X'),
    (2, 'A'),
    (3, 'A'),
    (3, 'A'),
    (3, 'B');
```

### Expected output

| id |
| --- |
| 3 |

[SQL solution](SOLUTIONS.md#q27-find-customers-whose-basket-exactly-equals-the-required-set) · [PySpark solution](SOLUTIONS.md#pyspark-q27)

## Q28 Find pairs of customers with identical baskets including empty ones

**Pattern:** Relational division and set equality

**Difficulty:** Hard

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

Return customer pairs a < b whose distinct baskets are identical. Include pairs of empty baskets. Product keys are non-null; repeated basket rows count once.

### Sample data

**customers**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |

**basket**

| customer_id | product |
| --- | --- |
| 1 | A |
| 1 | A |
| 1 | B |
| 2 | B |
| 2 | A |
| 3 | A |

### SQL setup

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY
);

INSERT INTO customers (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5);

CREATE TABLE basket (
    customer_id INTEGER,
    product TEXT
);

INSERT INTO basket (customer_id, product) VALUES
    (1, 'A'),
    (1, 'A'),
    (1, 'B'),
    (2, 'B'),
    (2, 'A'),
    (3, 'A');
```

### Expected output

| a | b |
| --- | --- |
| 1 | 2 |
| 4 | 5 |

[SQL solution](SOLUTIONS.md#q28-find-pairs-of-customers-with-identical-baskets-including-empty-ones) · [PySpark solution](SOLUTIONS.md#pyspark-q28)

## Q29 Find students who never scored an exam extreme

**Pattern:** Universal conditions and exclusion

**Difficulty:** Hard

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

A quiet student took at least one exam and never tied for the minimum or maximum score in any exam they took. Return quiet student IDs. Scores are non-null and unique by student and exam. Students with no exams are excluded.

### Sample data

**students**

| id |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |

**scores**

| exam_id | student_id | score |
| --- | --- | --- |
| 1 | 1 | 10 |
| 1 | 2 | 20 |
| 1 | 3 | 30 |
| 1 | 4 | 30 |
| 2 | 1 | 40 |
| 2 | 2 | 50 |
| 2 | 3 | 60 |
| 2 | 4 | 50 |

### SQL setup

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY
);

INSERT INTO students (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5);

CREATE TABLE scores (
    exam_id INTEGER,
    student_id INTEGER,
    score INTEGER
);

INSERT INTO scores (exam_id, student_id, score) VALUES
    (1, 1, 10),
    (1, 2, 20),
    (1, 3, 30),
    (1, 4, 30),
    (2, 1, 40),
    (2, 2, 50),
    (2, 3, 60),
    (2, 4, 50);
```

### Expected output

| id |
| --- |
| 2 |

[SQL solution](SOLUTIONS.md#q29-find-students-who-never-scored-an-exam-extreme) · [PySpark solution](SOLUTIONS.md#pyspark-q29)

## Q30 Combine duplicate and unique conditions at different grains

**Pattern:** Independent grouping grains

**Difficulty:** Hard

Adapted pattern with fresh integer amounts. Source pattern: [LeetCode Investments in 2016](https://leetcode.com/problems/investments-in-2016/).

Sum current_value for policies whose prior_value occurs more than once across all policies, but whose (lat,lon) pair occurs exactly once across all policies. Locations and values are non-null.

### Sample data

**policies**

| id | prior_value | current_value | lat | lon |
| --- | --- | --- | --- | --- |
| 1 | 10 | 5 | 1 | 1 |
| 2 | 20 | 20 | 2 | 2 |
| 3 | 10 | 30 | 2 | 2 |
| 4 | 10 | 40 | 4 | 4 |
| 5 | 99 | 7 | 5 | 5 |

### SQL setup

```sql
CREATE TABLE policies (
    id INTEGER PRIMARY KEY,
    prior_value INTEGER,
    current_value INTEGER,
    lat INTEGER,
    lon INTEGER
);

INSERT INTO policies (id, prior_value, current_value, lat, lon) VALUES
    (1, 10, 5, 1, 1),
    (2, 20, 20, 2, 2),
    (3, 10, 30, 2, 2),
    (4, 10, 40, 4, 4),
    (5, 99, 7, 5, 5);
```

### Expected output

| total |
| --- |
| 45 |

[SQL solution](SOLUTIONS.md#q30-combine-duplicate-and-unique-conditions-at-different-grains) · [PySpark solution](SOLUTIONS.md#pyspark-q30)

## Q31 Explain peer expansion in ROWS versus RANGE

**Pattern:** Window frames and peer rows

**Difficulty:** Medium

Original semantics exercise. Pattern reference: [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/functions-window.html).

Return each transaction with two cumulative sums: row_total follows (at,id) one row at a time; peer_total includes every transaction with timestamp <= the current timestamp. The two transactions at time 1 must share peer_total.

### Sample data

**tx**

| id | at | amount |
| --- | --- | --- |
| 1 | 1 | 10 |
| 2 | 1 | 20 |
| 3 | 2 | 5 |

### SQL setup

```sql
CREATE TABLE tx (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    amount INTEGER
);

INSERT INTO tx (id, at, amount) VALUES
    (1, 1, 10),
    (2, 1, 20),
    (3, 2, 5);
```

### Expected output

| id | row_total | peer_total |
| --- | --- | --- |
| 1 | 10 | 30 |
| 2 | 30 | 30 |
| 3 | 35 | 35 |

[SQL solution](SOLUTIONS.md#q31-explain-peer-expansion-in-rows-versus-range) · [PySpark solution](SOLUTIONS.md#pyspark-q31)

## Q32 Get the true last value rather than the last value so far

**Pattern:** Window frames and peer rows

**Difficulty:** Medium

Original semantics exercise. Pattern reference: [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/functions-window.html).

Return every event with the final value for its user. Final means greatest (at,id), and a final NULL must stay NULL. Do not collapse the event rows.

### Sample data

**events**

| id | user_id | at | val |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 10 |
| 2 | 1 | 2 | 5 |
| 3 | 2 | 1 | 7 |
| 4 | 2 | 2 | NULL |

### SQL setup

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    at INTEGER,
    val INTEGER
);

INSERT INTO events (id, user_id, at, val) VALUES
    (1, 1, 1, 10),
    (2, 1, 2, 5),
    (3, 2, 1, 7),
    (4, 2, 2, NULL);
```

### Expected output

| id | final_value |
| --- | --- |
| 1 | 5 |
| 2 | 5 |
| 3 | NULL |
| 4 | NULL |

[SQL solution](SOLUTIONS.md#q32-get-the-true-last-value-rather-than-the-last-value-so-far) · [PySpark solution](SOLUTIONS.md#pyspark-q32)

## Q33 Forward fill NULLs even when values decrease

**Pattern:** Window frames and missing values

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

For each user, carry the latest non-null value forward in timestamp and ID order. Leading NULLs remain NULL. Values may decrease or be negative.

### Sample data

**readings**

| id | user_id | at | val |
| --- | --- | --- | --- |
| 1 | 1 | 1 | NULL |
| 2 | 1 | 2 | 10 |
| 3 | 1 | 3 | NULL |
| 4 | 1 | 4 | 3 |
| 5 | 1 | 5 | NULL |
| 6 | 2 | 1 | -2 |
| 7 | 2 | 2 | NULL |

### SQL setup

```sql
CREATE TABLE readings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    at INTEGER,
    val INTEGER
);

INSERT INTO readings (id, user_id, at, val) VALUES
    (1, 1, 1, NULL),
    (2, 1, 2, 10),
    (3, 1, 3, NULL),
    (4, 1, 4, 3),
    (5, 1, 5, NULL),
    (6, 2, 1, -2),
    (7, 2, 2, NULL);
```

### Expected output

| id | filled_value |
| --- | --- |
| 1 | NULL |
| 2 | 10 |
| 3 | 10 |
| 4 | 3 |
| 5 | 3 |
| 6 | -2 |
| 7 | -2 |

[SQL solution](SOLUTIONS.md#q33-forward-fill-nulls-even-when-values-decrease) · [PySpark solution](SOLUTIONS.md#pyspark-q33)

## Q34 Compute a calendar rolling average with missing days

**Pattern:** Calendar completion and rolling windows

**Difficulty:** Hard

Original extension with missing days and a shorter window. Pattern reference: [LeetCode Restaurant Growth](https://leetcode.com/problems/restaurant-growth/).

For report days 1 through 5, return complete three-calendar-day windows ending at days 3,4,5. Missing days have zero revenue. Multiple sales per day must first aggregate. Return day, window_total, and average rounded to two decimals.

### Sample data

**sales**

| id | day_no | amount |
| --- | --- | --- |
| 1 | 1 | 10 |
| 2 | 1 | 20 |
| 3 | 3 | 60 |
| 4 | 5 | 30 |

### SQL setup

```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    day_no INTEGER,
    amount INTEGER
);

INSERT INTO sales (id, day_no, amount) VALUES
    (1, 1, 10),
    (2, 1, 20),
    (3, 3, 60),
    (4, 5, 30);
```

### Expected output

| day_no | window_total | average |
| --- | --- | --- |
| 3 | 90 | 30.0 |
| 4 | 60 | 20.0 |
| 5 | 90 | 30.0 |

[SQL solution](SOLUTIONS.md#q34-compute-a-calendar-rolling-average-with-missing-days) · [PySpark solution](SOLUTIONS.md#pyspark-q34)

## Q35 Count distinct active users across a rolling calendar window

**Pattern:** Calendar completion and rolling windows

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

Return distinct active users for each report day 1 through 4, considering that day and the previous two calendar days. Duplicate user events count once. There are no events before day 1.

### Sample data

**calendar**

| day_no |
| --- |
| 1 |
| 2 |
| 3 |
| 4 |

**activity**

| user_id | day_no |
| --- | --- |
| 1 | 1 |
| 1 | 2 |
| 1 | 2 |
| 2 | 2 |
| 3 | 4 |

### SQL setup

```sql
CREATE TABLE calendar (
    day_no INTEGER PRIMARY KEY
);

INSERT INTO calendar (day_no) VALUES
    (1),
    (2),
    (3),
    (4);

CREATE TABLE activity (
    user_id INTEGER,
    day_no INTEGER
);

INSERT INTO activity (user_id, day_no) VALUES
    (1, 1),
    (1, 2),
    (1, 2),
    (2, 2),
    (3, 4);
```

### Expected output

| day_no | active_users |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |

[SQL solution](SOLUTIONS.md#q35-count-distinct-active-users-across-a-rolling-calendar-window) · [PySpark solution](SOLUTIONS.md#pyspark-q35)

## Q36 Maintain a cumulative distinct count without a distinct window aggregate

**Pattern:** Window frames and missing values

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

In (at,id) event order, return the cumulative number of distinct non-null user IDs seen. NULL users contribute nothing. Repeated users do not increase the total.

### Sample data

**events**

| id | at | user_id |
| --- | --- | --- |
| 1 | 1 | 8 |
| 2 | 1 | 8 |
| 3 | 2 | 9 |
| 4 | 3 | NULL |
| 5 | 4 | 8 |
| 6 | 5 | 10 |

### SQL setup

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    at INTEGER,
    user_id INTEGER
);

INSERT INTO events (id, at, user_id) VALUES
    (1, 1, 8),
    (2, 1, 8),
    (3, 2, 9),
    (4, 3, NULL),
    (5, 4, 8),
    (6, 5, 10);
```

### Expected output

| id | distinct_users |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 2 |
| 5 | 2 |
| 6 | 3 |

[SQL solution](SOLUTIONS.md#q36-maintain-a-cumulative-distinct-count-without-a-distinct-window-aggregate) · [PySpark solution](SOLUTIONS.md#pyspark-q36)

## Q37 Compute group medians without losing duplicate observations

**Pattern:** Order statistics and weighted distributions

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Return the numeric median salary per company, averaging the two central observations for even-size groups. Equal salaries are separate observations. Salaries are non-null.

### Sample data

**employees**

| id | company | salary |
| --- | --- | --- |
| 1 | A | 10 |
| 2 | A | 10 |
| 3 | A | 30 |
| 4 | A | 90 |
| 5 | B | 5 |
| 6 | B | 15 |
| 7 | B | 100 |

### SQL setup

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    company TEXT,
    salary INTEGER
);

INSERT INTO employees (id, company, salary) VALUES
    (1, 'A', 10),
    (2, 'A', 10),
    (3, 'A', 30),
    (4, 'A', 90),
    (5, 'B', 5),
    (6, 'B', 15),
    (7, 'B', 100);
```

### Expected output

| company | median |
| --- | --- |
| A | 20.0 |
| B | 15.0 |

[SQL solution](SOLUTIONS.md#q37-compute-group-medians-without-losing-duplicate-observations) · [PySpark solution](SOLUTIONS.md#pyspark-q37)

## Q38 Find the median from value frequencies without expanding rows

**Pattern:** Order statistics and weighted distributions

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Return the median of the represented multiset. Each frequency is a positive integer; value keys are unique. Avoid generating one row per observation.

### Sample data

**frequencies**

| val | freq |
| --- | --- |
| 10 | 2 |
| 20 | 1 |
| 30 | 3 |

### SQL setup

```sql
CREATE TABLE frequencies (
    val INTEGER PRIMARY KEY,
    freq INTEGER
);

INSERT INTO frequencies (val, freq) VALUES
    (10, 2),
    (20, 1),
    (30, 3);
```

### Expected output

| median |
| --- |
| 25.0 |

[SQL solution](SOLUTIONS.md#q38-find-the-median-from-value-frequencies-without-expanding-rows) · [PySpark solution](SOLUTIONS.md#pyspark-q38)

## Q39 Find the last person in a capacity limited boarding prefix

**Pattern:** Prefix constraints and cumulative state

**Difficulty:** Medium

Adapted problem with fresh data and explicit stop semantics. Source pattern: [LeetCode Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/).

People board in ascending turn. Boarding stops at the first person who would exceed capacity 1000; later lighter people cannot skip ahead. Weights are positive and turns are unique. Return the final admitted person, or no row if nobody fits.

### Sample data

**queue**

| turn | name | weight |
| --- | --- | --- |
| 1 | Ana | 400 |
| 2 | Ben | 350 |
| 3 | Cy | 250 |
| 4 | Di | 1 |
| 5 | Eli | 10 |

### SQL setup

```sql
CREATE TABLE queue (
    turn INTEGER PRIMARY KEY,
    name TEXT,
    weight INTEGER
);

INSERT INTO queue (turn, name, weight) VALUES
    (1, 'Ana', 400),
    (2, 'Ben', 350),
    (3, 'Cy', 250),
    (4, 'Di', 1),
    (5, 'Eli', 10);
```

### Expected output

| turn | name |
| --- | --- |
| 3 | Cy |

[SQL solution](SOLUTIONS.md#q39-find-the-last-person-in-a-capacity-limited-boarding-prefix) · [PySpark solution](SOLUTIONS.md#pyspark-q39)

## Q40 Reset running totals at reset events

**Pattern:** Prefix constraints and cumulative state

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Return each event with its accumulated amount since the most recent reset. Reset rows have amount zero and reset the displayed total to zero. Amounts may be negative. Events have a unique sequence number.

### Sample data

**events**

| seq | is_reset | amount |
| --- | --- | --- |
| 1 | 0 | 5 |
| 2 | 0 | 3 |
| 3 | 1 | 0 |
| 4 | 0 | 4 |
| 5 | 0 | -1 |
| 6 | 1 | 0 |
| 7 | 0 | 2 |

### SQL setup

```sql
CREATE TABLE events (
    seq INTEGER PRIMARY KEY,
    is_reset INTEGER,
    amount INTEGER
);

INSERT INTO events (seq, is_reset, amount) VALUES
    (1, 0, 5),
    (2, 0, 3),
    (3, 1, 0),
    (4, 0, 4),
    (5, 0, -1),
    (6, 1, 0),
    (7, 0, 2);
```

### Expected output

| seq | running_total |
| --- | --- |
| 1 | 5 |
| 2 | 8 |
| 3 | 0 |
| 4 | 4 |
| 5 | 3 |
| 6 | 0 |
| 7 | 2 |

[SQL solution](SOLUTIONS.md#q40-reset-running-totals-at-reset-events) · [PySpark solution](SOLUTIONS.md#pyspark-q40)

## Q41 Detect repeated values by row adjacency rather than ID arithmetic

**Pattern:** Gaps and islands

**Difficulty:** Medium

Original extension distinguishing row adjacency from consecutive IDs. Pattern reference: [LeetCode Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/).

Return non-null values appearing in at least three consecutive observations ordered by seq. seq is unique but may have gaps. Consecutive means adjacent rows, not seq + 1. Return each qualifying value once.

### Sample data

**logs**

| seq | val |
| --- | --- |
| 10 | 7 |
| 20 | 7 |
| 40 | 7 |
| 50 | 8 |
| 60 | 7 |
| 70 | 8 |
| 80 | 8 |
| 90 | 8 |

### SQL setup

```sql
CREATE TABLE logs (
    seq INTEGER PRIMARY KEY,
    val INTEGER
);

INSERT INTO logs (seq, val) VALUES
    (10, 7),
    (20, 7),
    (40, 7),
    (50, 8),
    (60, 7),
    (70, 8),
    (80, 8),
    (90, 8);
```

### Expected output

| val |
| --- |
| 7 |
| 8 |

[SQL solution](SOLUTIONS.md#q41-detect-repeated-values-by-row-adjacency-rather-than-id-arithmetic) · [PySpark solution](SOLUTIONS.md#pyspark-q41)

## Q42 Swap neighboring seats when seat IDs are sparse

**Pattern:** Positional pairing

**Difficulty:** Hard

Original extension using position rather than ID parity. Pattern reference: [LeetCode Exchange Seats](https://leetcode.com/problems/exchange-seats/).

Order seats by seat_id and swap the occupants of each neighboring pair. Keep seat IDs fixed. An odd last occupant stays. Seat IDs need not start at 1 or be consecutive; occupants are non-null.

### Sample data

**seats**

| seat_id | occupant |
| --- | --- |
| 10 | Ana |
| 20 | Ben |
| 40 | Cy |
| 70 | Di |
| 90 | Eli |

### SQL setup

```sql
CREATE TABLE seats (
    seat_id INTEGER PRIMARY KEY,
    occupant TEXT
);

INSERT INTO seats (seat_id, occupant) VALUES
    (10, 'Ana'),
    (20, 'Ben'),
    (40, 'Cy'),
    (70, 'Di'),
    (90, 'Eli');
```

### Expected output

| seat_id | occupant |
| --- | --- |
| 10 | Ben |
| 20 | Ana |
| 40 | Di |
| 70 | Cy |
| 90 | Eli |

[SQL solution](SOLUTIONS.md#q42-swap-neighboring-seats-when-seat-ids-are-sparse) · [PySpark solution](SOLUTIONS.md#pyspark-q42)

## Q43 Choose tournament winners when players occupy either match column

**Pattern:** Role unpivoting and tie rules

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

Return the winning player for every group by total match score. A player can appear as either first_player or second_player. Include registered players with no matches as zero. Break total-score ties by smaller player ID. Each match belongs within one group.

### Sample data

**players**

| id | group_id |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 2 |

**matches**

| id | first_player | second_player | first_score | second_score |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 1 |
| 2 | 2 | 3 | 2 | 3 |

### SQL setup

```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    group_id INTEGER
);

INSERT INTO players (id, group_id) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    first_player INTEGER,
    second_player INTEGER,
    first_score INTEGER,
    second_score INTEGER
);

INSERT INTO matches (id, first_player, second_player, first_score, second_score) VALUES
    (1, 1, 2, 3, 1),
    (2, 2, 3, 2, 3);
```

### Expected output

| group_id | winner_id | score |
| --- | --- | --- |
| 1 | 1 | 3 |
| 2 | 4 | 0 |

[SQL solution](SOLUTIONS.md#q43-choose-tournament-winners-when-players-occupy-either-match-column) · [PySpark solution](SOLUTIONS.md#pyspark-q43)

## Q44 Compute cohort retention with a fixed signup denominator

**Pattern:** Grain and denominator traps

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

Return day-one retention for each signup-day cohort: the fraction of its registered users with at least one activity exactly one day after signup. Duplicate activity rows count once; inactive users stay in the denominator. Round to two decimals.

### Sample data

**users**

| id | signup_day |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 2 |

**activity**

| user_id | day_no |
| --- | --- |
| 1 | 2 |
| 1 | 2 |
| 2 | 3 |
| 4 | 3 |
| 5 | 3 |

### SQL setup

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    signup_day INTEGER
);

INSERT INTO users (id, signup_day) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2);

CREATE TABLE activity (
    user_id INTEGER,
    day_no INTEGER
);

INSERT INTO activity (user_id, day_no) VALUES
    (1, 2),
    (1, 2),
    (2, 3),
    (4, 3),
    (5, 3);
```

### Expected output

| signup_day | retention |
| --- | --- |
| 1 | 0.33 |
| 2 | 1.0 |

[SQL solution](SOLUTIONS.md#q44-compute-cohort-retention-with-a-fixed-signup-denominator) · [PySpark solution](SOLUTIONS.md#pyspark-q44)

## Q45 Find consecutive over limit months across a year boundary

**Pattern:** Calendar adjacency and preaggregation

**Difficulty:** Hard

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

Return accounts whose credited total exceeds their limit in two consecutive calendar months. month_index is year*12 + month-1, so December and January are adjacent. Aggregate credits by account and month first. Missing months are not over-limit; equals the limit is not over-limit.

### Sample data

**accounts**

| id | monthly_limit |
| --- | --- |
| 1 | 100 |
| 2 | 100 |
| 3 | 100 |

**credits**

| account_id | month_index | amount |
| --- | --- | --- |
| 1 | 24299 | 60 |
| 1 | 24299 | 60 |
| 1 | 24300 | 110 |
| 2 | 24299 | 120 |
| 2 | 24301 | 130 |
| 3 | 24299 | 100 |
| 3 | 24300 | 150 |

### SQL setup

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    monthly_limit INTEGER
);

INSERT INTO accounts (id, monthly_limit) VALUES
    (1, 100),
    (2, 100),
    (3, 100);

CREATE TABLE credits (
    account_id INTEGER,
    month_index INTEGER,
    amount INTEGER
);

INSERT INTO credits (account_id, month_index, amount) VALUES
    (1, 24299, 60),
    (1, 24299, 60),
    (1, 24300, 110),
    (2, 24299, 120),
    (2, 24301, 130),
    (3, 24299, 100),
    (3, 24300, 150);
```

### Expected output

| account_id |
| --- |
| 1 |

[SQL solution](SOLUTIONS.md#q45-find-consecutive-over-limit-months-across-a-year-boundary) · [PySpark solution](SOLUTIONS.md#pyspark-q45)

## Q46 Find all descendants without looping on cyclic relationships

**Pattern:** Recursive reachability

**Difficulty:** Hard

Original practice exercise. Pattern reference: [PostgreSQL Recursive Queries](https://www.postgresql.org/docs/current/queries-with.html).

Return all IDs reachable below manager 1 through the reports edges, excluding manager 1 itself. Data can be cyclic and duplicated; an employee may have more than one incoming edge.

### Sample data

**reports**

| manager_id | employee_id |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 1 |
| 2 | 4 |
| 1 | 2 |
| 5 | 6 |

### SQL setup

```sql
CREATE TABLE reports (
    manager_id INTEGER,
    employee_id INTEGER
);

INSERT INTO reports (manager_id, employee_id) VALUES
    (1, 2),
    (2, 3),
    (3, 1),
    (2, 4),
    (1, 2),
    (5, 6);
```

### Expected output

| id |
| --- |
| 2 |
| 3 |
| 4 |

[SQL solution](SOLUTIONS.md#q46-find-all-descendants-without-looping-on-cyclic-relationships) · [PySpark solution](SOLUTIONS.md#pyspark-q46)

## Q47 Classify tree nodes with root precedence

**Pattern:** Hierarchy classification

**Difficulty:** Medium

Adapted pattern with multiple rooted trees including a singleton. Source pattern: [LeetCode Tree Node](https://leetcode.com/problems/tree-node/).

Classify each node Root, Inner, or Leaf. A root has no parent and must be Root even if it has no children. The input is a valid forest with non-null IDs and nullable parent_id.

### Sample data

**nodes**

| id | parent_id |
| --- | --- |
| 1 | NULL |
| 2 | 1 |
| 3 | 1 |
| 4 | 2 |
| 9 | NULL |

### SQL setup

```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER
);

INSERT INTO nodes (id, parent_id) VALUES
    (1, NULL),
    (2, 1),
    (3, 1),
    (4, 2),
    (9, NULL);
```

### Expected output

| id | node_type |
| --- | --- |
| 1 | Root |
| 2 | Inner |
| 3 | Leaf |
| 4 | Leaf |
| 9 | Root |

[SQL solution](SOLUTIONS.md#q47-classify-tree-nodes-with-root-precedence) · [PySpark solution](SOLUTIONS.md#pyspark-q47)

## Q48 Find ordered funnel completions rather than mere event presence

**Pattern:** Ordered event matching

**Difficulty:** Hard

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

Return users who have a view, then a later add, then a later buy. Timestamps must strictly increase. Repeated attempts are allowed and any valid sequence qualifies. Merely having all three event kinds is insufficient.

### Sample data

**events**

| id | user_id | kind | at |
| --- | --- | --- | --- |
| 1 | 1 | view | 1 |
| 2 | 1 | buy | 2 |
| 3 | 1 | add | 3 |
| 4 | 1 | buy | 4 |
| 5 | 2 | buy | 1 |
| 6 | 2 | add | 2 |
| 7 | 2 | view | 3 |
| 8 | 3 | view | 1 |
| 9 | 3 | add | 1 |
| 10 | 3 | buy | 2 |

### SQL setup

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    kind TEXT,
    at INTEGER
);

INSERT INTO events (id, user_id, kind, at) VALUES
    (1, 1, 'view', 1),
    (2, 1, 'buy', 2),
    (3, 1, 'add', 3),
    (4, 1, 'buy', 4),
    (5, 2, 'buy', 1),
    (6, 2, 'add', 2),
    (7, 2, 'view', 3),
    (8, 3, 'view', 1),
    (9, 3, 'add', 1),
    (10, 3, 'buy', 2);
```

### Expected output

| user_id |
| --- |
| 1 |

[SQL solution](SOLUTIONS.md#q48-find-ordered-funnel-completions-rather-than-mere-event-presence) · [PySpark solution](SOLUTIONS.md#pyspark-q48)

## Q49 Allocate supply to demand in FIFO order without a cursor

**Pattern:** Cumulative interval matching and FIFO

**Difficulty:** Hard

Adapted allocation pattern with fresh data. Source pattern: [Itzik Ben Gan Matching Supply With Demand Challenge](https://sqlperformance.com/2021/12/t-sql-queries/supply-demand-challenge).

Supplies are available before all demands. Consume supplies and fulfill demands in ascending ID order. Quantities are positive and total supply is sufficient. Return demand_id, supply_id, and allocated quantity for every nonzero allocation.

### Sample data

**supplies**

| id | qty |
| --- | --- |
| 1 | 5 |
| 2 | 4 |
| 3 | 6 |

**demands**

| id | qty |
| --- | --- |
| 1 | 7 |
| 2 | 5 |

### SQL setup

```sql
CREATE TABLE supplies (
    id INTEGER PRIMARY KEY,
    qty INTEGER
);

INSERT INTO supplies (id, qty) VALUES
    (1, 5),
    (2, 4),
    (3, 6);

CREATE TABLE demands (
    id INTEGER PRIMARY KEY,
    qty INTEGER
);

INSERT INTO demands (id, qty) VALUES
    (1, 7),
    (2, 5);
```

### Expected output

| demand_id | supply_id | allocated |
| --- | --- | --- |
| 1 | 1 | 5 |
| 1 | 2 | 2 |
| 2 | 2 | 2 |
| 2 | 3 | 3 |

[SQL solution](SOLUTIONS.md#q49-allocate-supply-to-demand-in-fifo-order-without-a-cursor) · [PySpark solution](SOLUTIONS.md#pyspark-q49)

## Q50 Value remaining FIFO inventory with a partially consumed batch

**Pattern:** Cumulative interval matching and FIFO

**Difficulty:** Hard

Simplified adaptation with no returns or backorders. Source pattern: [Kathi Kellenberger FIFO Stock Inventory](https://www.red-gate.com/simple-talk/databases/sql-server/performance-sql-server/set-based-speed-phreakery-the-fifo-stock-inventory-sql-problem/).

For each product, return remaining quantity and FIFO inventory value after all movements. IN rows have positive quantity and a unit cost; OUT rows have positive quantity and NULL cost. IDs define chronology. Inventory never goes negative. There are no returns. Equal costs do not identify equal batches.

### Sample data

**movements**

| id | product | kind | qty | cost |
| --- | --- | --- | --- | --- |
| 1 | A | IN | 5 | 10 |
| 2 | A | IN | 4 | 20 |
| 3 | A | OUT | 7 | NULL |
| 4 | A | IN | 6 | 30 |
| 5 | A | OUT | 5 | NULL |
| 6 | B | IN | 2 | 7 |
| 7 | B | OUT | 2 | NULL |

### SQL setup

```sql
CREATE TABLE movements (
    id INTEGER PRIMARY KEY,
    product TEXT,
    kind TEXT,
    qty INTEGER,
    cost INTEGER
);

INSERT INTO movements (id, product, kind, qty, cost) VALUES
    (1, 'A', 'IN', 5, 10),
    (2, 'A', 'IN', 4, 20),
    (3, 'A', 'OUT', 7, NULL),
    (4, 'A', 'IN', 6, 30),
    (5, 'A', 'OUT', 5, NULL),
    (6, 'B', 'IN', 2, 7),
    (7, 'B', 'OUT', 2, NULL);
```

### Expected output

| product | remaining_qty | inventory_value |
| --- | --- | --- |
| A | 3 | 90 |
| B | 0 | 0 |

[SQL solution](SOLUTIONS.md#q50-value-remaining-fifo-inventory-with-a-partially-consumed-batch) · [PySpark solution](SOLUTIONS.md#pyspark-q50)
