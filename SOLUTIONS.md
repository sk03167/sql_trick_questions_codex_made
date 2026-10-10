# SQL Trick Question Solutions

Each solution answers the corresponding exercise in [QUESTIONS.md](QUESTIONS.md). Read the question contract first: duplicate identity, time boundaries, allowed ties, missing rows, and NULL meaning determine whether the SQL is correct.

## Dialect and data conventions

- Tested reference dialect: SQLite 3.28 or newer. The recorded verification run uses SQLite 3.53.4. No database server or third-party package is required.
- Integer `/` in the median queries must truncate for integer operands; `3.0` and `1.0` force fractional arithmetic where required. Adapt with FLOOR or integer division in another dialect.
- SQL Server: remove the RECURSIVE keyword, use TOP or OFFSET/FETCH instead of LIMIT, use an appropriate string type instead of TEXT, and apply the engine recursion limits deliberately. Recursive UNION-based cycle handling needs a different implementation because SQL Server recursive CTE syntax and restrictions differ.
- PostgreSQL: these CASE-based endpoint comparisons avoid reliance on SQLite scalar MIN/MAX. PostgreSQL offers LEAST/GREATEST and IS DISTINCT FROM as conveniences. This catalog does not claim engine-by-engine execution testing.
- MySQL: use 8.0 or newer for window functions and recursive CTEs; median integer divisions need DIV or FLOOR.
- Spark SQL: date and interval arithmetic differs, and recursive support depends on runtime. Treat the recursive exercises as requiring a supported engine or an explicit iterative implementation.
- Text comparisons follow the database collation. Endpoints in the pair exercises are non-null and must use a consistent collation.
- day_no denotes consecutive calendar-day ordinals; minute_no denotes elapsed-minute ordinals. month_index = year*12 + month-1. Convert actual DATE/TIMESTAMP data with dialect-appropriate functions and a declared timezone.
- [start,end) intervals include start and exclude end. Positive-length intervals are assumed.
- Fixture DDL is intentionally small; production constraints, indexes, and query plans must match real workload contracts.

## Solution index

| ID | Solution | Pattern |
| --- | --- | --- |
| Q01 | [Deduplicate reverse routes while preserving an original row](#q01-deduplicate-reverse-routes-while-preserving-an-original-row) | Unordered pairs and symmetry breaking |
| Q02 | [Find reciprocal pairs without matching a row to itself](#q02-find-reciprocal-pairs-without-matching-a-row-to-itself) | Unordered pairs and symmetry breaking |
| Q03 | [Count undirected neighbors despite duplicated edge directions](#q03-count-undirected-neighbors-despite-duplicated-edge-directions) | Graph edge normalization |
| Q04 | [Find graph triangles exactly once](#q04-find-graph-triangles-exactly-once) | Graph edge normalization |
| Q05 | [Assign connected components including isolated nodes](#q05-assign-connected-components-including-isolated-nodes) | Recursive reachability |
| Q06 | [Compress integer sequences with duplicate input values](#q06-compress-integer-sequences-with-duplicate-input-values) | Gaps and islands |
| Q07 | [Find every longest login streak with duplicate logins](#q07-find-every-longest-login-streak-with-duplicate-logins) | Gaps and islands |
| Q08 | [Find missing ranges including the boundaries](#q08-find-missing-ranges-including-the-boundaries) | Gaps and islands |
| Q09 | [Sessionize events with an exact inactivity threshold](#q09-sessionize-events-with-an-exact-inactivity-threshold) | Sessionization and change points |
| Q10 | [Group status runs with NULL states and missing days](#q10-group-status-runs-with-null-states-and-missing-days) | Sessionization and change points |
| Q11 | [Return every row in qualifying ID streaks](#q11-return-every-row-in-qualifying-id-streaks) | Gaps and islands |
| Q12 | [Reconstruct projects from one day tasks](#q12-reconstruct-projects-from-one-day-tasks) | Gaps and islands |
| Q13 | [Merge overlapping intervals even when they are nested](#q13-merge-overlapping-intervals-even-when-they-are-nested) | Interval packing and sweep lines |
| Q14 | [Find free time between overlapping bookings](#q14-find-free-time-between-overlapping-bookings) | Interval packing and sweep lines |
| Q15 | [Find peak simultaneous meetings with tied event times](#q15-find-peak-simultaneous-meetings-with-tied-event-times) | Interval packing and sweep lines |
| Q16 | [Measure occupied duration without counting overlaps twice](#q16-measure-occupied-duration-without-counting-overlaps-twice) | Interval packing and sweep lines |
| Q17 | [Resolve prices as of a date while keeping products without history](#q17-resolve-prices-as-of-a-date-while-keeping-products-without-history) | Temporal and nearest joins |
| Q18 | [Join facts to effective dated dimensions at a shared boundary](#q18-join-facts-to-effective-dated-dimensions-at-a-shared-boundary) | Temporal and nearest joins |
| Q19 | [Choose the closest observation with a deterministic tie rule](#q19-choose-the-closest-observation-with-a-deterministic-tie-rule) | Temporal and nearest joins |
| Q20 | [Find nonbuyers when the purchase table contains NULL](#q20-find-nonbuyers-when-the-purchase-table-contains-null) | NULL semantics and anti joins |
| Q21 | [Keep parents that have no qualifying child rows](#q21-keep-parents-that-have-no-qualifying-child-rows) | NULL semantics and anti joins |
| Q22 | [Aggregate orders and payments without join fan out](#q22-aggregate-orders-and-payments-without-join-fan-out) | Join grain and multiplicity |
| Q23 | [Preserve independent transaction amounts when duplicate values are valid](#q23-preserve-independent-transaction-amounts-when-duplicate-values-are-valid) | Join grain and multiplicity |
| Q24 | [Reconcile two snapshots including NULL valued changes](#q24-reconcile-two-snapshots-including-null-valued-changes) | Set and multiset reconciliation |
| Q25 | [Reconcile duplicate counts rather than just distinct rows](#q25-reconcile-duplicate-counts-rather-than-just-distinct-rows) | Set and multiset reconciliation |
| Q26 | [Find customers covering every required product](#q26-find-customers-covering-every-required-product) | Relational division and set equality |
| Q27 | [Find customers whose basket exactly equals the required set](#q27-find-customers-whose-basket-exactly-equals-the-required-set) | Relational division and set equality |
| Q28 | [Find pairs of customers with identical baskets including empty ones](#q28-find-pairs-of-customers-with-identical-baskets-including-empty-ones) | Relational division and set equality |
| Q29 | [Find students who never scored an exam extreme](#q29-find-students-who-never-scored-an-exam-extreme) | Universal conditions and exclusion |
| Q30 | [Combine duplicate and unique conditions at different grains](#q30-combine-duplicate-and-unique-conditions-at-different-grains) | Independent grouping grains |
| Q31 | [Explain peer expansion in ROWS versus RANGE](#q31-explain-peer-expansion-in-rows-versus-range) | Window frames and peer rows |
| Q32 | [Get the true last value rather than the last value so far](#q32-get-the-true-last-value-rather-than-the-last-value-so-far) | Window frames and peer rows |
| Q33 | [Forward fill NULLs even when values decrease](#q33-forward-fill-nulls-even-when-values-decrease) | Window frames and missing values |
| Q34 | [Compute a calendar rolling average with missing days](#q34-compute-a-calendar-rolling-average-with-missing-days) | Calendar completion and rolling windows |
| Q35 | [Count distinct active users across a rolling calendar window](#q35-count-distinct-active-users-across-a-rolling-calendar-window) | Calendar completion and rolling windows |
| Q36 | [Maintain a cumulative distinct count without a distinct window aggregate](#q36-maintain-a-cumulative-distinct-count-without-a-distinct-window-aggregate) | Window frames and missing values |
| Q37 | [Compute group medians without losing duplicate observations](#q37-compute-group-medians-without-losing-duplicate-observations) | Order statistics and weighted distributions |
| Q38 | [Find the median from value frequencies without expanding rows](#q38-find-the-median-from-value-frequencies-without-expanding-rows) | Order statistics and weighted distributions |
| Q39 | [Find the last person in a capacity limited boarding prefix](#q39-find-the-last-person-in-a-capacity-limited-boarding-prefix) | Prefix constraints and cumulative state |
| Q40 | [Reset running totals at reset events](#q40-reset-running-totals-at-reset-events) | Prefix constraints and cumulative state |
| Q41 | [Detect repeated values by row adjacency rather than ID arithmetic](#q41-detect-repeated-values-by-row-adjacency-rather-than-id-arithmetic) | Gaps and islands |
| Q42 | [Swap neighboring seats when seat IDs are sparse](#q42-swap-neighboring-seats-when-seat-ids-are-sparse) | Positional pairing |
| Q43 | [Choose tournament winners when players occupy either match column](#q43-choose-tournament-winners-when-players-occupy-either-match-column) | Role unpivoting and tie rules |
| Q44 | [Compute cohort retention with a fixed signup denominator](#q44-compute-cohort-retention-with-a-fixed-signup-denominator) | Grain and denominator traps |
| Q45 | [Find consecutive over limit months across a year boundary](#q45-find-consecutive-over-limit-months-across-a-year-boundary) | Calendar adjacency and preaggregation |
| Q46 | [Find all descendants without looping on cyclic relationships](#q46-find-all-descendants-without-looping-on-cyclic-relationships) | Recursive reachability |
| Q47 | [Classify tree nodes with root precedence](#q47-classify-tree-nodes-with-root-precedence) | Hierarchy classification |
| Q48 | [Find ordered funnel completions rather than mere event presence](#q48-find-ordered-funnel-completions-rather-than-mere-event-presence) | Ordered event matching |
| Q49 | [Allocate supply to demand in FIFO order without a cursor](#q49-allocate-supply-to-demand-in-fifo-order-without-a-cursor) | Cumulative interval matching and FIFO |
| Q50 | [Value remaining FIFO inventory with a partially consumed batch](#q50-value-remaining-fifo-inventory-with-a-partially-consumed-batch) | Cumulative interval matching and FIFO |

## Q01 Deduplicate reverse routes while preserving an original row

**Pattern:** Unordered pairs and symmetry breaking

[Question and dataset](QUESTIONS.md#q01-deduplicate-reverse-routes-while-preserving-an-original-row)

```sql
WITH canonical AS (
  SELECT *, CASE WHEN src <= dst THEN src ELSE dst END AS lo,
            CASE WHEN src <= dst THEN dst ELSE src END AS hi
  FROM routes
), keep AS (
  SELECT MIN(row_id) AS row_id FROM canonical GROUP BY lo, hi, dist
)
SELECT r.row_id, r.src, r.dst, r.dist
FROM routes r JOIN keep k ON r.row_id = k.row_id
ORDER BY r.row_id;
```

### Why it works

Canonical endpoints define the duplicate key, but joining retained IDs back to the source preserves original direction. The distance belongs to the key because the prompt says different distances are distinct.

### The trap

WHERE src < dst loses the lone D to C route and every self route. DISTINCT on the original columns does not normalize direction.

### Alternative LEFT self anti join

```sql
SELECT a.row_id, a.src, a.dst, a.dist
FROM routes a
LEFT JOIN routes b
  ON b.row_id < a.row_id AND b.dist = a.dist
 AND ((b.src = a.src AND b.dst = a.dst)
   OR (b.src = a.dst AND b.dst = a.src))
WHERE b.row_id IS NULL
ORDER BY a.row_id;
```

### Expected output

| row_id | src | dst | dist |
| --- | --- | --- | --- |
| 1 | A | B | 10 |
| 3 | A | C | 5 |
| 4 | D | C | 7 |
| 6 | A | A | 0 |
| 7 | B | A | 12 |

### Interview follow up

If distance is excluded from the key, which conflicting distance should survive?

Original extension of a symmetric pair pattern. Pattern reference: [HackerRank Symmetric Pairs](https://www.hackerrank.com/challenges/symmetric-pairs/problem).

## Q02 Find reciprocal pairs without matching a row to itself

**Pattern:** Unordered pairs and symmetry breaking

[Question and dataset](QUESTIONS.md#q02-find-reciprocal-pairs-without-matching-a-row-to-itself)

```sql
SELECT DISTINCT a.x, a.y
FROM pairs a JOIN pairs b
  ON a.x = b.y AND a.y = b.x AND a.id <> b.id
WHERE a.x <= a.y
ORDER BY a.x, a.y;
```

### Why it works

The ID inequality forces a different physical row. The endpoint inequality picks one orientation; DISTINCT handles repeated witnesses.

### The trap

A self join on endpoints alone incorrectly certifies the single (3,3) row as reciprocal.

### Expected output

| x | y |
| --- | --- |
| 1 | 2 |
| 4 | 4 |

### Interview follow up

Without a row ID, how would grouping and counts distinguish one self pair from two?

Adapted practice problem with fresh data. Source pattern: [HackerRank Symmetric Pairs](https://www.hackerrank.com/challenges/symmetric-pairs/problem).

## Q03 Count undirected neighbors despite duplicated edge directions

**Pattern:** Graph edge normalization

[Question and dataset](QUESTIONS.md#q03-count-undirected-neighbors-despite-duplicated-edge-directions)

```sql
WITH directed AS (
  SELECT a AS person, b AS neighbor FROM edges WHERE a <> b
  UNION
  SELECT b, a FROM edges WHERE a <> b
)
SELECT p.id, COUNT(d.neighbor) AS neighbors
FROM people p LEFT JOIN directed d ON d.person = p.id
GROUP BY p.id ORDER BY p.id;
```

### Why it works

UNION constructs a set of directed neighbor relationships. The master people table retains isolated vertices.

### The trap

UNION ALL counts duplicate edges. COUNT(*) gives an isolated person a count of one after a LEFT JOIN.

### Expected output

| id | neighbors |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |

### Interview follow up

How would you return actual mutual friends between two people instead of degrees?

Original extension of a published bidirectional friendship problem. Pattern reference: [LeetCode Friend Requests II](https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/).

## Q04 Find graph triangles exactly once

**Pattern:** Graph edge normalization

[Question and dataset](QUESTIONS.md#q04-find-graph-triangles-exactly-once)

```sql
WITH e AS (
  SELECT DISTINCT CASE WHEN src < dst THEN src ELSE dst END AS a,
                  CASE WHEN src < dst THEN dst ELSE src END AS b
  FROM edges WHERE src <> dst
)
SELECT x.a, x.b, y.b AS c
FROM e x JOIN e y ON x.b = y.a
JOIN e z ON z.a = x.a AND z.b = y.b
ORDER BY x.a, x.b, y.b;
```

### Why it works

Canonical edges enforce a strict vertex order. Two joined edges form a path; the third join closes it.

### The trap

Three unrestricted self joins return permutations of the same triangle. A two-edge path is not a triangle.

### Expected output

| a | b | c |
| --- | --- | --- |
| 1 | 2 | 3 |
| 1 | 3 | 4 |

### Interview follow up

How would directed cycles differ from undirected triangles?

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

## Q05 Assign connected components including isolated nodes

**Pattern:** Recursive reachability

[Question and dataset](QUESTIONS.md#q05-assign-connected-components-including-isolated-nodes)

```sql
WITH RECURSIVE e(a,b) AS (
  SELECT a,b FROM edges UNION SELECT b,a FROM edges
), reach(root,node) AS (
  SELECT id,id FROM nodes
  UNION
  SELECT r.root,e.b FROM reach r JOIN e ON e.a=r.node
)
SELECT node, MIN(root) AS component
FROM reach GROUP BY node ORDER BY node;
```

### Why it works

Start from every node and expand reachability. UNION deduplicates the complete (root,node) state, allowing finite termination on cycles.

### The trap

UNION ALL loops on cycles. Adding an ever-increasing depth to the deduplication state would defeat cycle termination.

### Expected output

| node | component |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 4 |
| 5 | 4 |
| 6 | 6 |

### Interview follow up

What changes if you need shortest paths instead of reachability?

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

## Q06 Compress integer sequences with duplicate input values

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q06-compress-integer-sequences-with-duplicate-input-values)

```sql
WITH d AS (SELECT DISTINCT value FROM observations),
g AS (SELECT value, value-ROW_NUMBER() OVER (ORDER BY value) AS island FROM d)
SELECT MIN(value) AS start_value, MAX(value) AS end_value, COUNT(*) AS length
FROM g GROUP BY island ORDER BY start_value;
```

### Why it works

After deduplication, value and row number increase together inside a run, so their difference is constant.

### The trap

Numbering duplicate values first splits a legitimate run. Grouping by value alone does not identify adjacency.

### Alternative Boundary flags instead of row-number subtraction

```sql
WITH d AS (SELECT DISTINCT value FROM observations),
p AS (SELECT value,LAG(value) OVER (ORDER BY value) AS prev FROM d),
g AS (SELECT value,SUM(CASE WHEN prev IS NULL OR value<>prev+1 THEN 1 ELSE 0 END)
      OVER (ORDER BY value ROWS UNBOUNDED PRECEDING) AS island FROM p)
SELECT MIN(value) AS start_value,MAX(value) AS end_value,COUNT(*) AS length
FROM g GROUP BY island ORDER BY start_value;
```

### Expected output

| start_value | end_value | length |
| --- | --- | --- |
| 1 | 3 | 3 |
| 7 | 8 | 2 |
| 10 | 10 | 1 |

### Interview follow up

How would you change the break condition if a gap of two were allowed?

Original practice extension of contiguous grouping. Pattern reference: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

## Q07 Find every longest login streak with duplicate logins

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q07-find-every-longest-login-streak-with-duplicate-logins)

```sql
WITH d AS (SELECT DISTINCT user_id,day_no FROM logins),
g AS (
  SELECT *,day_no-ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day_no) AS island FROM d
), streaks AS (
  SELECT user_id,MIN(day_no) AS start_day,MAX(day_no) AS end_day,COUNT(*) AS days
  FROM g GROUP BY user_id,island
), ranked AS (
  SELECT *,MAX(days) OVER (PARTITION BY user_id) AS longest FROM streaks
)
SELECT user_id,start_day,end_day,days FROM ranked
WHERE days=longest ORDER BY user_id,start_day;
```

### Why it works

First build streaks, then compare their lengths within each user. Comparing against the maximum keeps both equally long streaks.

### The trap

ROW_NUMBER() = 1 over streak length arbitrarily discards ties. YYYYMMDD subtraction is not calendar arithmetic.

### Expected output

| user_id | start_day | end_day | days |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 2 |
| 1 | 4 | 5 | 2 |
| 2 | 2 | 4 | 3 |

### Interview follow up

For actual DATE columns, what date arithmetic does your SQL dialect require?

Original practice extension. Pattern reference: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

## Q08 Find missing ranges including the boundaries

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q08-find-missing-ranges-including-the-boundaries)

```sql
WITH points AS (
  SELECT 0 AS id UNION SELECT id FROM ids UNION SELECT 13
), n AS (SELECT id,LEAD(id) OVER (ORDER BY id) AS next_id FROM points)
SELECT id+1 AS gap_start,next_id-1 AS gap_end
FROM n WHERE next_id > id+1 ORDER BY gap_start;
```

### Why it works

Sentinels just outside the allowed range expose both boundary gaps. LEAD gives each neighboring pair of observed points.

### The trap

Looking only between existing rows misses the beginning and end. Expanding every absent number can be expensive for large ranges.

### Expected output

| gap_start | gap_end |
| --- | --- |
| 1 | 2 |
| 5 | 7 |
| 9 | 9 |
| 11 | 12 |

### Interview follow up

What should happen when the input is empty? The answer should be the entire allowed range.

Original practice extension. Pattern reference: [SQLite WITH and recursive graph queries](https://www.sqlite.org/lang_with.html).

## Q09 Sessionize events with an exact inactivity threshold

**Pattern:** Sessionization and change points

[Question and dataset](QUESTIONS.md#q09-sessionize-events-with-an-exact-inactivity-threshold)

```sql
WITH p AS (
  SELECT *,LAG(minute_no) OVER (PARTITION BY user_id ORDER BY minute_no,event_id) AS prev FROM events
), f AS (
  SELECT *,CASE WHEN prev IS NULL OR minute_no-prev>30 THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (PARTITION BY user_id ORDER BY minute_no,event_id ROWS UNBOUNDED PRECEDING) AS session_no FROM f
)
SELECT user_id,session_no,MIN(minute_no) AS start_minute,MAX(minute_no) AS end_minute,COUNT(*) AS events
FROM g GROUP BY user_id,session_no ORDER BY user_id,session_no;
```

### Why it works

LAG measures inactivity between adjacent events; a running sum of break flags labels sessions.

### The trap

Using >= 30 changes the exact boundary. Bucketing by minute_no / 30 ignores activity chains that cross fixed bucket boundaries.

### Expected output

| user_id | session_no | start_minute | end_minute | events |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 30 | 2 |
| 1 | 2 | 61 | 61 | 2 |
| 2 | 1 | 5 | 5 | 1 |
| 2 | 2 | 40 | 40 | 1 |

### Interview follow up

Should late-arriving events be allowed to merge two sessions that were already published?

Adapted pattern with fresh data and explicit boundary semantics. Source pattern: [Ryan Guill Aggregating event data into sessions](https://ryanguill.com/postgresql/sql/2024/06/24/aggregating-event-data-into-sessions.html).

## Q10 Group status runs with NULL states and missing days

**Pattern:** Sessionization and change points

[Question and dataset](QUESTIONS.md#q10-group-status-runs-with-null-states-and-missing-days)

```sql
WITH p AS (
  SELECT *,LAG(day_no) OVER (ORDER BY day_no) AS prev_day,
           LAG(status) OVER (ORDER BY day_no) AS prev_status FROM daily
), f AS (
  SELECT *,CASE WHEN day_no=prev_day+1 AND
    (status=prev_status OR (status IS NULL AND prev_status IS NULL))
    THEN 0 ELSE 1 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY day_no ROWS UNBOUNDED PRECEDING) AS island FROM f
)
SELECT status,MIN(day_no) AS start_day,MAX(day_no) AS end_day
FROM g GROUP BY island,status ORDER BY start_day;
```

### Why it works

A boundary depends on both calendar adjacency and null-aware state equality. Explicitly handling NULL preserves the intended unknown-state run.

### The trap

status <> LAG(status) evaluates to unknown around NULLs. Grouping only by status merges separated runs.

### Expected output

| status | start_day | end_day |
| --- | --- | --- |
| up | 1 | 2 |
| NULL | 3 | 4 |
| NULL | 6 | 6 |
| up | 7 | 7 |

### Interview follow up

How should conflicting status observations for the same day be resolved?

Original practice extension. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q11 Return every row in qualifying ID streaks

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q11-return-every-row-in-qualifying-id-streaks)

```sql
WITH g AS (
  SELECT *,id-ROW_NUMBER() OVER (ORDER BY id) AS island
  FROM visits WHERE people>=100
), c AS (SELECT *,COUNT(*) OVER (PARTITION BY island) AS run_length FROM g)
SELECT id,day_no,people FROM c WHERE run_length>=3 ORDER BY id;
```

### Why it works

Filter qualifying observations before deriving ID islands. A window count labels every row with its island size.

### The trap

Calendar-date gaps are irrelevant here. Returning only each island boundary omits required interior rows.

### Expected output

| id | day_no | people |
| --- | --- | --- |
| 5 | 5 | 130 |
| 6 | 6 | 140 |
| 7 | 9 | 150 |

### Interview follow up

What changes when the interviewer asks for consecutive dates instead of IDs?

Adapted problem with fresh data. Source pattern: [LeetCode Human Traffic of Stadium](https://leetcode.com/problems/human-traffic-of-stadium/).

## Q12 Reconstruct projects from one day tasks

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q12-reconstruct-projects-from-one-day-tasks)

```sql
WITH g AS (
  SELECT *,start_day-ROW_NUMBER() OVER (ORDER BY start_day) AS island FROM tasks
)
SELECT MIN(start_day) AS project_start,MAX(end_day) AS project_end,
       MAX(end_day)-MIN(start_day) AS duration
FROM g GROUP BY island ORDER BY duration,project_start;
```

### Why it works

The one-day, non-overlapping contract turns project reconstruction into integer islands on task starts.

### The trap

This arithmetic shortcut fails when tasks have variable durations or overlap; interval packing is then required.

### Expected output

| project_start | project_end | duration |
| --- | --- | --- |
| 5 | 6 | 1 |
| 1 | 3 | 2 |
| 8 | 11 | 3 |

### Interview follow up

Would touching tasks still form a project if end boundaries were inclusive?

Adapted problem with fresh data. Source pattern: [HackerRank SQL Project Planning](https://www.hackerrank.com/challenges/sql-projects/problem).

## Q13 Merge overlapping intervals even when they are nested

**Pattern:** Interval packing and sweep lines

[Question and dataset](QUESTIONS.md#q13-merge-overlapping-intervals-even-when-they-are-nested)

```sql
WITH p AS (
  SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS previous_max
  FROM intervals
), f AS (
  SELECT *,CASE WHEN previous_max IS NULL OR start_at>previous_max THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS island FROM f
)
SELECT MIN(start_at) AS start_at,MAX(end_at) AS end_at
FROM g GROUP BY island ORDER BY start_at;
```

### Why it works

Compare each start with the largest prior end, not merely the previous row end. That prior envelope remembers long intervals even after short nested ones.

### The trap

LAG(end_at) sees 3 before the interval starting at 4 and incorrectly splits coverage still protected by [1,10).

### Expected output

| start_at | end_at |
| --- | --- |
| 1 | 12 |
| 15 | 17 |

### Interview follow up

Change > to >= if touching intervals should remain separate. Partition all windows when intervals belong to different resources.

Adapted pattern with a nested-interval counterexample. Source pattern: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

## Q14 Find free time between overlapping bookings

**Pattern:** Interval packing and sweep lines

[Question and dataset](QUESTIONS.md#q14-find-free-time-between-overlapping-bookings)

```sql
WITH p AS (
  SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS mx FROM bookings
), f AS (
  SELECT *,CASE WHEN mx IS NULL OR start_at>mx THEN 1 ELSE 0 END AS fresh FROM p
), g AS (
  SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS grp FROM f
), packed AS (
  SELECT MIN(start_at) AS s,MAX(end_at) AS e FROM g GROUP BY grp
), padded AS (
  SELECT s,e FROM packed UNION ALL SELECT 0,0 UNION ALL SELECT 20,20
), gaps AS (
  SELECT e AS free_start,LEAD(s) OVER (ORDER BY s,e) AS free_end FROM padded
)
SELECT free_start,free_end FROM gaps WHERE free_end>free_start ORDER BY free_start;
```

### Why it works

Pack occupied coverage before taking its complement. Boundary sentinels expose free time before the first booking and after the last.

### The trap

Taking LEAD directly over raw bookings invents free intervals inside overlapping bookings.

### Expected output

| free_start | free_end |
| --- | --- |
| 0 | 1 |
| 7 | 10 |
| 16 | 20 |

### Interview follow up

How would you clip bookings that start before 0 or end after 20?

Original practice extension. Pattern reference: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

## Q15 Find peak simultaneous meetings with tied event times

**Pattern:** Interval packing and sweep lines

[Question and dataset](QUESTIONS.md#q15-find-peak-simultaneous-meetings-with-tied-event-times)

```sql
WITH events AS (
  SELECT start_at AS at,1 AS delta FROM meetings
  UNION ALL SELECT end_at,-1 FROM meetings
), grouped AS (SELECT at,SUM(delta) AS delta FROM events GROUP BY at),
swept AS (
  SELECT at,LEAD(at) OVER (ORDER BY at) AS until,
         SUM(delta) OVER (ORDER BY at ROWS UNBOUNDED PRECEDING) AS active
  FROM grouped
), segments AS (SELECT * FROM swept WHERE until>at),
peaks AS (SELECT *,MAX(active) OVER () AS peak FROM segments)
SELECT at AS start_at,until AS end_at,active FROM peaks WHERE active=peak ORDER BY at;
```

### Why it works

Collapse simultaneous starts and ends into one net change. The running active count applies to the interval from that time to the next event.

### The trap

Processing starts before ends can create a fake zero-duration peak. Counting overlapping pairs is not a concurrency measure.

### Expected output

| start_at | end_at | active |
| --- | --- | --- |
| 4 | 5 | 3 |

### Interview follow up

If meetings use closed intervals, what must change at equal endpoints?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q16 Measure occupied duration without counting overlaps twice

**Pattern:** Interval packing and sweep lines

[Question and dataset](QUESTIONS.md#q16-measure-occupied-duration-without-counting-overlaps-twice)

```sql
WITH p AS (
  SELECT *,MAX(e) OVER (ORDER BY s,e,id ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS mx FROM ranges
), f AS (SELECT *,CASE WHEN mx IS NULL OR s>mx THEN 1 ELSE 0 END AS fresh FROM p),
g AS (SELECT *,SUM(fresh) OVER (ORDER BY s,e,id ROWS UNBOUNDED PRECEDING) AS grp FROM f),
packed AS (SELECT MIN(s) AS s,MAX(e) AS e FROM g GROUP BY grp)
SELECT COALESCE(SUM(e-s),0) AS occupied FROM packed;
```

### Why it works

Pack the union of coverage, then measure the disjoint ranges. COALESCE gives zero when there are no intervals.

### The trap

SUM(end-start) measures total booked effort, not unique occupied time.

### Expected output

| occupied |
| --- |
| 14 |

### Interview follow up

Can you compute the same measure from sweep-line segments where active > 0?

Original practice extension. Pattern reference: [C R Timmons SQL Packing Intervals](https://www.crtimmonsinc.com/2018/05/04/packing-intervals/).

## Q17 Resolve prices as of a date while keeping products without history

**Pattern:** Temporal and nearest joins

[Question and dataset](QUESTIONS.md#q17-resolve-prices-as-of-a-date-while-keeping-products-without-history)

```sql
WITH eligible AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY day_no DESC) AS rn
  FROM changes WHERE day_no<=5
)
SELECT p.id,COALESCE(e.price,10) AS price
FROM products p LEFT JOIN eligible e ON e.product_id=p.id AND e.rn=1
ORDER BY p.id;
```

### Why it works

Restrict history to the as-of boundary before choosing a row. Driving from the master preserves future-only and history-free products. Stored prices are non-null.

### The trap

Ranking all history first and then filtering the newest row by date can erase the valid earlier price.

### Alternative Correlated latest eligible change

```sql
SELECT p.id,COALESCE((
  SELECT c.price FROM changes c WHERE c.product_id=p.id AND c.day_no<=5
  ORDER BY c.day_no DESC LIMIT 1
),10) AS price FROM products p ORDER BY p.id;
```

### Expected output

| id | price |
| --- | --- |
| 1 | 30 |
| 2 | 10 |
| 3 | 15 |
| 4 | 10 |

### Interview follow up

If a stored price can be NULL, why must you test row existence rather than COALESCE(price,10)?

Adapted pattern with fresh data and a product master. Source pattern: [LeetCode Product Price at a Given Date](https://leetcode.com/problems/product-price-at-a-given-date/).

## Q18 Join facts to effective dated dimensions at a shared boundary

**Pattern:** Temporal and nearest joins

[Question and dataset](QUESTIONS.md#q18-join-facts-to-effective-dated-dimensions-at-a-shared-boundary)

```sql
SELECT f.id,v.label
FROM facts f LEFT JOIN versions v
  ON v.key_id=f.key_id AND f.at>=v.valid_from
 AND (f.at<v.valid_to OR v.valid_to IS NULL)
ORDER BY f.id;
```

### Why it works

The lower bound is inclusive and the upper bound exclusive. Put eligibility in ON so uncovered facts survive.

### The trap

BETWEEN includes both ends and matches the fact at 5 to two versions.

### Expected output

| id | label |
| --- | --- |
| 1 | old |
| 2 | new |
| 3 | latest |
| 4 | NULL |

### Interview follow up

How would you detect overlapping dimension periods before trusting this join?

Original practice exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

## Q19 Choose the closest observation with a deterministic tie rule

**Pattern:** Temporal and nearest joins

[Question and dataset](QUESTIONS.md#q19-choose-the-closest-observation-with-a-deterministic-tie-rule)

```sql
WITH candidates AS (
  SELECT t.id AS target_id,r.id AS reading_id,r.at,r.value,
    ROW_NUMBER() OVER (PARTITION BY t.id ORDER BY ABS(t.at-r.at),r.at,r.id) AS rn
  FROM targets t CROSS JOIN readings r
)
SELECT target_id,reading_id,value FROM candidates WHERE rn=1 ORDER BY target_id;
```

### Why it works

The ordering expresses all tie-breakers. This exhaustive candidate version favors clarity for small examples, not production-scale efficiency.

### The trap

MIN(ABS(...)) alone can return multiple tied candidates. Ordering by distance alone leaves the winner unspecified.

### Expected output

| target_id | reading_id | value |
| --- | --- | --- |
| 1 | 1 | 30 |
| 2 | 4 | 120 |
| 3 | 1 | 30 |

### Interview follow up

At scale, how could predecessor and successor seeks avoid a full cross join?

Adapted pattern with fresh data. Source pattern: [Itzik Ben Gan Closest Match Part 1](https://sqlperformance.com/2018/12/t-sql-queries/closest-match-part-1).

## Q20 Find nonbuyers when the purchase table contains NULL

**Pattern:** NULL semantics and anti joins

[Question and dataset](QUESTIONS.md#q20-find-nonbuyers-when-the-purchase-table-contains-null)

```sql
SELECT c.id FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM purchases p WHERE p.customer_id=c.id)
ORDER BY c.id;
```

### Why it works

NOT EXISTS asks whether a matching row exists, so the unrelated NULL key cannot poison the result.

### The trap

id NOT IN (SELECT customer_id FROM purchases) yields unknown for nonmatching IDs when the subquery contains NULL.

### Alternative LEFT anti join

```sql
SELECT c.id FROM customers c
LEFT JOIN purchases p ON p.customer_id=c.id
WHERE p.id IS NULL ORDER BY c.id;
```

### Expected output

| id |
| --- |
| 2 |
| 3 |

### Interview follow up

How would you implement the same anti join with LEFT JOIN and a non-nullable purchase ID?

Original semantics exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

## Q21 Keep parents that have no qualifying child rows

**Pattern:** NULL semantics and anti joins

[Question and dataset](QUESTIONS.md#q21-keep-parents-that-have-no-qualifying-child-rows)

```sql
SELECT c.id,COUNT(o.id) AS paid_orders
FROM customers c LEFT JOIN orders o
  ON o.customer_id=c.id AND o.status='paid'
GROUP BY c.id ORDER BY c.id;
```

### Why it works

Apply the child eligibility predicate in ON. Count the child key, not the null-extended parent row.

### The trap

WHERE o.status='paid' after the LEFT JOIN eliminates customers 2 and 3. WHERE status='paid' OR status IS NULL still loses customer 2.

### Expected output

| id | paid_orders |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |

### Interview follow up

Why does the OR status IS NULL workaround fail when nonqualifying child rows exist?

Original semantics exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

## Q22 Aggregate orders and payments without join fan out

**Pattern:** Join grain and multiplicity

[Question and dataset](QUESTIONS.md#q22-aggregate-orders-and-payments-without-join-fan-out)

```sql
WITH o AS (SELECT customer_id,SUM(amount) AS total FROM orders GROUP BY customer_id),
p AS (SELECT customer_id,SUM(amount) AS total FROM payments GROUP BY customer_id)
SELECT c.id,COALESCE(o.total,0) AS ordered,COALESCE(p.total,0) AS paid
FROM customers c LEFT JOIN o ON o.customer_id=c.id
LEFT JOIN p ON p.customer_id=c.id ORDER BY c.id;
```

### Why it works

Reduce each child independently to one row per customer before joining. This makes both measures live at the same grain.

### The trap

The raw join creates 2 x 3 rows for customer 1. SUM(DISTINCT amount) undercounts legitimate equal-value orders and payments.

### Expected output

| id | ordered | paid |
| --- | --- | --- |
| 1 | 100 | 100 |
| 2 | 0 | 0 |

### Interview follow up

How would you add refunds as a third independent child without multiplying rows?

Original practice exercise. Pattern reference: [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

## Q23 Preserve independent transaction amounts when duplicate values are valid

**Pattern:** Join grain and multiplicity

[Question and dataset](QUESTIONS.md#q23-preserve-independent-transaction-amounts-when-duplicate-values-are-valid)

```sql
SELECT COALESCE(SUM(i.amount),0) AS approved_total
FROM invoices i WHERE EXISTS (
  SELECT 1 FROM tags t WHERE t.invoice_id=i.id AND t.tag='approved'
);
```

### Why it works

EXISTS tests eligibility without expanding invoice rows. The sum therefore counts invoice identities rather than distinct numeric values.

### The trap

SUM after a raw join returns 150; SUM(DISTINCT amount) returns 50. Both are wrong for opposite reasons.

### Alternative Deduplicate eligible identities before aggregating

```sql
WITH eligible AS (
  SELECT DISTINCT invoice_id FROM tags WHERE tag='approved'
)
SELECT COALESCE(SUM(i.amount),0) AS approved_total
FROM invoices i JOIN eligible e ON e.invoice_id=i.id;
```

### Expected output

| approved_total |
| --- |
| 100 |

### Interview follow up

How would you return qualifying invoice detail without relying on DISTINCT?

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

## Q24 Reconcile two snapshots including NULL valued changes

**Pattern:** Set and multiset reconciliation

[Question and dataset](QUESTIONS.md#q24-reconcile-two-snapshots-including-null-valued-changes)

```sql
SELECT o.id AS id,CASE WHEN n.id IS NULL THEN 'removed' ELSE 'changed' END AS change_kind,
       o.val AS old_value,n.val AS new_value
FROM old_snapshot o LEFT JOIN new_snapshot n ON n.id=o.id
WHERE n.id IS NULL OR o.val<>n.val
   OR (o.val IS NULL AND n.val IS NOT NULL)
   OR (o.val IS NOT NULL AND n.val IS NULL)
UNION ALL
SELECT n.id,'added',NULL,n.val
FROM new_snapshot n LEFT JOIN old_snapshot o ON o.id=n.id
WHERE o.id IS NULL
ORDER BY id;
```

### Why it works

Two disjoint LEFT JOIN branches emulate a full comparison. Presence is tested using the primary key; value differences explicitly include NULL transitions.

### The trap

old.val <> new.val misses NULL changes. COALESCE to a magic string conflates real data with a sentinel.

### Expected output

| id | change_kind | old_value | new_value |
| --- | --- | --- | --- |
| 2 | changed | NULL | b |
| 3 | removed | c | NULL |
| 4 | added | NULL | d |

### Interview follow up

On PostgreSQL, how would FULL OUTER JOIN and IS DISTINCT FROM shorten the query?

Original practice exercise. Pattern reference: [SQLite SQL Expressions](https://www.sqlite.org/lang_expr.html).

## Q25 Reconcile duplicate counts rather than just distinct rows

**Pattern:** Set and multiset reconciliation

[Question and dataset](QUESTIONS.md#q25-reconcile-duplicate-counts-rather-than-just-distinct-rows)

```sql
WITH signed AS (
  SELECT key_name,-1 AS delta FROM old_bag
  UNION ALL SELECT key_name,1 FROM new_bag
)
SELECT key_name,SUM(delta) AS delta FROM signed
GROUP BY key_name HAVING SUM(delta)<>0
ORDER BY CASE WHEN key_name IS NULL THEN 0 ELSE 1 END,key_name;
```

### Why it works

Treat every old occurrence as minus one and every new occurrence as plus one, then add per key. GROUP BY also collects NULL keys together.

### The trap

EXCEPT with distinct semantics can hide multiplicity changes for a and b. UNION would erase repeated signed occurrences.

### Expected output

| key_name | delta |
| --- | --- |
| NULL | 1 |
| a | -1 |
| b | 1 |
| c | 1 |

### Interview follow up

How would you return actual surplus physical rows if the bags also had stable row IDs?

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

## Q26 Find customers covering every required product

**Pattern:** Relational division and set equality

[Question and dataset](QUESTIONS.md#q26-find-customers-covering-every-required-product)

```sql
SELECT c.id FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM required r WHERE NOT EXISTS (
    SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND p.product=r.product
  )
) ORDER BY c.id;
```

### Why it works

Double NOT EXISTS says there is no required product missing from this customer. It naturally handles duplicate purchases and an empty requirement set.

### The trap

Counting all purchased products can confuse duplicates or extras with coverage. Starting from purchases loses customers with no purchases under empty requirements.

### Alternative Count coverage after intersecting with requirements

```sql
SELECT c.id FROM customers c
LEFT JOIN purchases p ON p.customer_id=c.id
LEFT JOIN required r ON r.product=p.product
GROUP BY c.id
HAVING COUNT(DISTINCT r.product)=(SELECT COUNT(*) FROM required)
ORDER BY c.id;
```

### Expected output

| id |
| --- |
| 1 |
| 3 |

### Interview follow up

Why is the empty-set result called vacuous truth? When might the business rule deliberately reject it?

Adapted pattern with duplicates, extras, and a master table. Source pattern: [LeetCode Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/).

## Q27 Find customers whose basket exactly equals the required set

**Pattern:** Relational division and set equality

[Question and dataset](QUESTIONS.md#q27-find-customers-whose-basket-exactly-equals-the-required-set)

```sql
SELECT c.id FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM required r WHERE NOT EXISTS (
    SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND p.product=r.product
  )
) AND NOT EXISTS (
  SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND NOT EXISTS (
    SELECT 1 FROM required r WHERE r.product=p.product
  )
) ORDER BY c.id;
```

### Why it works

Set equality needs containment in both directions. Coverage alone permits customer 1, whose basket includes X.

### The trap

Matching the count of distinct products is insufficient: a basket {A,X} has the same cardinality as {A,B}.

### Expected output

| id |
| --- |
| 3 |

### Interview follow up

With empty requirements, only customers with empty baskets should qualify.

Original extension from containment to equality. Pattern reference: [LeetCode Customers Who Bought All Products](https://leetcode.com/problems/customers-who-bought-all-products/).

## Q28 Find pairs of customers with identical baskets including empty ones

**Pattern:** Relational division and set equality

[Question and dataset](QUESTIONS.md#q28-find-pairs-of-customers-with-identical-baskets-including-empty-ones)

```sql
SELECT a.id AS a,b.id AS b FROM customers a JOIN customers b ON a.id<b.id
WHERE NOT EXISTS (
  SELECT 1 FROM basket x WHERE x.customer_id=a.id AND NOT EXISTS (
    SELECT 1 FROM basket y WHERE y.customer_id=b.id AND y.product=x.product
  )
) AND NOT EXISTS (
  SELECT 1 FROM basket y WHERE y.customer_id=b.id AND NOT EXISTS (
    SELECT 1 FROM basket x WHERE x.customer_id=a.id AND x.product=y.product
  )
) ORDER BY a.id,b.id;
```

### Why it works

Compare missing members in both directions for every candidate pair. Empty baskets pass both tests without special serialization.

### The trap

Concatenating products can collide, depend on ordering, or silently drop empty baskets. Equal counts do not establish equal contents.

### Expected output

| a | b |
| --- | --- |
| 1 | 2 |
| 4 | 5 |

### Interview follow up

How would you change this to compare multisets where duplicate quantities matter?

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

## Q29 Find students who never scored an exam extreme

**Pattern:** Universal conditions and exclusion

[Question and dataset](QUESTIONS.md#q29-find-students-who-never-scored-an-exam-extreme)

```sql
WITH limits AS (
  SELECT exam_id,MIN(score) AS lo,MAX(score) AS hi FROM scores GROUP BY exam_id
)
SELECT s.id FROM students s
WHERE EXISTS (SELECT 1 FROM scores x WHERE x.student_id=s.id)
  AND NOT EXISTS (
    SELECT 1 FROM scores x JOIN limits l ON l.exam_id=x.exam_id
    WHERE x.student_id=s.id AND (x.score=l.lo OR x.score=l.hi)
  ) ORDER BY s.id;
```

### Why it works

First derive each exam extreme, then exclude anyone appearing at either extreme in any exam. The participation check excludes student 5.

### The trap

Filtering individual non-extreme rows still leaves student 4 because they were non-extreme in exam 2 but maximal in exam 1.

### Expected output

| id |
| --- |
| 2 |

### Interview follow up

In an exam with one participant, that participant is both minimum and maximum.

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

## Q30 Combine duplicate and unique conditions at different grains

**Pattern:** Independent grouping grains

[Question and dataset](QUESTIONS.md#q30-combine-duplicate-and-unique-conditions-at-different-grains)

```sql
WITH flagged AS (
  SELECT *,COUNT(*) OVER (PARTITION BY prior_value) AS prior_count,
           COUNT(*) OVER (PARTITION BY lat,lon) AS location_count FROM policies
)
SELECT COALESCE(SUM(current_value),0) AS total FROM flagged
WHERE prior_count>1 AND location_count=1;
```

### Why it works

Compute independent frequencies on the original population. Both flags must hold for a policy to contribute.

### The trap

Filtering by duplicated prior value before counting locations makes policy 3 appear unique because policy 2 has already been removed.

### Expected output

| total |
| --- |
| 45 |

### Interview follow up

Why can concatenating latitude and longitude be an unsafe grouping key?

Adapted pattern with fresh integer amounts. Source pattern: [LeetCode Investments in 2016](https://leetcode.com/problems/investments-in-2016/).

## Q31 Explain peer expansion in ROWS versus RANGE

**Pattern:** Window frames and peer rows

[Question and dataset](QUESTIONS.md#q31-explain-peer-expansion-in-rows-versus-range)

```sql
SELECT id,
  SUM(amount) OVER (ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS row_total,
  SUM(amount) OVER (ORDER BY at RANGE UNBOUNDED PRECEDING) AS peer_total
FROM tx ORDER BY at,id;
```

### Why it works

ROWS follows individual row positions under a total ordering. RANGE treats equal ordering values as peers.

### The trap

Adding id to the RANGE ordering changes peer groups. Leaving the frame implicit may produce timestamp-wide jumps when row-by-row accumulation was intended.

### Expected output

| id | row_total | peer_total |
| --- | --- | --- |
| 1 | 10 | 30 |
| 2 | 30 | 30 |
| 3 | 35 | 35 |

### Interview follow up

What total ordering is needed if two transactions share a timestamp?

Original semantics exercise. Pattern reference: [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/functions-window.html).

## Q32 Get the true last value rather than the last value so far

**Pattern:** Window frames and peer rows

[Question and dataset](QUESTIONS.md#q32-get-the-true-last-value-rather-than-the-last-value-so-far)

```sql
SELECT id,LAST_VALUE(val) OVER (
  PARTITION BY user_id ORDER BY at,id
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) AS final_value FROM events ORDER BY id;
```

### Why it works

The frame must reach the partition end. The function respects a genuinely NULL final observation.

### The trap

The default ordered frame ends at the current peer group, so LAST_VALUE often returns the current value. MAX is not the last value.

### Expected output

| id | final_value |
| --- | --- |
| 1 | 5 |
| 2 | 5 |
| 3 | NULL |
| 4 | NULL |

### Interview follow up

How would the question change if it asked for the last non-null value?

Original semantics exercise. Pattern reference: [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/functions-window.html).

## Q33 Forward fill NULLs even when values decrease

**Pattern:** Window frames and missing values

[Question and dataset](QUESTIONS.md#q33-forward-fill-nulls-even-when-values-decrease)

```sql
WITH g AS (
  SELECT *,COUNT(val) OVER (PARTITION BY user_id ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS grp FROM readings
)
SELECT id,MAX(val) OVER (PARTITION BY user_id,grp) AS filled_value FROM g ORDER BY id;
```

### Why it works

Each non-null value starts a new count group. Within a group there is exactly one non-null value, which MAX can propagate.

### The trap

A running MAX over the whole user keeps 10 after the real value decreases to 3.

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

### Interview follow up

If NULL means an explicit reset rather than missing data, is forward fill appropriate?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q34 Compute a calendar rolling average with missing days

**Pattern:** Calendar completion and rolling windows

[Question and dataset](QUESTIONS.md#q34-compute-a-calendar-rolling-average-with-missing-days)

```sql
WITH RECURSIVE calendar(day_no) AS (
  SELECT 1 UNION ALL SELECT day_no+1 FROM calendar WHERE day_no<5
), totals AS (SELECT day_no,SUM(amount) AS amount FROM sales GROUP BY day_no),
daily AS (
  SELECT c.day_no,COALESCE(t.amount,0) AS amount FROM calendar c LEFT JOIN totals t ON t.day_no=c.day_no
), rolled AS (
  SELECT day_no,SUM(amount) OVER (ORDER BY day_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS window_total FROM daily
)
SELECT day_no,window_total,ROUND(window_total/3.0,2) AS average
FROM rolled WHERE day_no>=3 ORDER BY day_no;
```

### Why it works

Densify the calendar and aggregate transaction grain before a row window. Only then do three rows mean three calendar days.

### The trap

Three preceding transactions or three observed days do not represent three calendar days. Filtering early removes window history.

### Expected output

| day_no | window_total | average |
| --- | --- | --- |
| 3 | 90 | 30.0 |
| 4 | 60 | 20.0 |
| 5 | 90 | 30.0 |

### Interview follow up

How would a real calendar table account for business days or daylight-saving boundaries?

Original extension with missing days and a shorter window. Pattern reference: [LeetCode Restaurant Growth](https://leetcode.com/problems/restaurant-growth/).

## Q35 Count distinct active users across a rolling calendar window

**Pattern:** Calendar completion and rolling windows

[Question and dataset](QUESTIONS.md#q35-count-distinct-active-users-across-a-rolling-calendar-window)

```sql
SELECT c.day_no,(
  SELECT COUNT(DISTINCT a.user_id) FROM activity a
  WHERE a.day_no BETWEEN c.day_no-2 AND c.day_no
) AS active_users FROM calendar c ORDER BY c.day_no;
```

### Why it works

Distinctness is evaluated over the whole window, not independently for each day. Correlation provides a clear portable reference solution.

### The trap

Summing daily distinct counts double-counts users active on multiple days. COUNT(DISTINCT ...) as a window aggregate is not available in every SQL engine.

### Expected output

| day_no | active_users |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 2 |
| 4 | 3 |

### Interview follow up

For large data, how could per-user active intervals and sweep lines avoid repeated scans?

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

## Q36 Maintain a cumulative distinct count without a distinct window aggregate

**Pattern:** Window frames and missing values

[Question and dataset](QUESTIONS.md#q36-maintain-a-cumulative-distinct-count-without-a-distinct-window-aggregate)

```sql
WITH marked AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY at,id) AS occurrence FROM events
)
SELECT id,SUM(CASE WHEN user_id IS NOT NULL AND occurrence=1 THEN 1 ELSE 0 END)
  OVER (ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS distinct_users
FROM marked ORDER BY at,id;
```

### Why it works

Mark only each user first occurrence, then accumulate those markers. The explicit NULL exclusion matches COUNT(DISTINCT user_id) semantics.

### The trap

A running count of events includes repeats. DENSE_RANK over user_id imposes user-value order, not first-arrival order.

### Expected output

| id | distinct_users |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 2 |
| 5 | 2 |
| 6 | 3 |

### Interview follow up

Why does first-occurrence marking fail for a sliding distinct window when old users leave the window?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q37 Compute group medians without losing duplicate observations

**Pattern:** Order statistics and weighted distributions

[Question and dataset](QUESTIONS.md#q37-compute-group-medians-without-losing-duplicate-observations)

```sql
WITH ordered AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary,id) AS rn,
           COUNT(*) OVER (PARTITION BY company) AS n FROM employees
)
SELECT company,AVG(salary*1.0) AS median FROM ordered
WHERE rn BETWEEN (n+1)/2 AND (n+2)/2
GROUP BY company ORDER BY company;
```

### Why it works

Integer division identifies one or two central row positions. A deterministic ID tie-break preserves observation identities.

### The trap

DENSE_RANK numbers distinct salary values rather than employees, changing the median when salaries repeat.

### Expected output

| company | median |
| --- | --- |
| A | 20.0 |
| B | 15.0 |

### Interview follow up

If you need the employee records at the median instead of a scalar median, what should be returned for even counts?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q38 Find the median from value frequencies without expanding rows

**Pattern:** Order statistics and weighted distributions

[Question and dataset](QUESTIONS.md#q38-find-the-median-from-value-frequencies-without-expanding-rows)

```sql
WITH bounds AS (
  SELECT val,freq,SUM(freq) OVER (ORDER BY val ROWS UNBOUNDED PRECEDING) AS hi,
                  SUM(freq) OVER () AS n FROM frequencies
), positions AS (
  SELECT (SUM(freq)+1)/2 AS p FROM frequencies
  UNION ALL SELECT (SUM(freq)+2)/2 FROM frequencies
)
SELECT AVG(b.val*1.0) AS median
FROM positions p JOIN bounds b ON p.p>b.hi-b.freq AND p.p<=b.hi;
```

### Why it works

Each value owns a cumulative rank interval. Locate both central positions within those intervals; UNION ALL retains two equal middle positions for odd counts.

### The trap

Taking the median of distinct values ignores frequency. Expanding very large frequencies wastes work.

### Expected output

| median |
| --- |
| 25.0 |

### Interview follow up

How would the rank target change for a percentile other than the median?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q39 Find the last person in a capacity limited boarding prefix

**Pattern:** Prefix constraints and cumulative state

[Question and dataset](QUESTIONS.md#q39-find-the-last-person-in-a-capacity-limited-boarding-prefix)

```sql
WITH totals AS (
  SELECT *,SUM(weight) OVER (ORDER BY turn ROWS UNBOUNDED PRECEDING) AS cumulative FROM queue
)
SELECT turn,name FROM totals WHERE cumulative<=1000 ORDER BY turn DESC LIMIT 1;
```

### Why it works

Positive weights make cumulative load monotonic, so eligible rows form a prefix. Descending turn chooses its final member.

### The trap

Filtering each person by individual weight does not enforce the shared capacity. The query relies on positivity and stop-at-first-failure semantics.

### Alternative Correlated prefix sum

```sql
SELECT q.turn,q.name FROM queue q
WHERE (SELECT SUM(p.weight) FROM queue p WHERE p.turn<=q.turn)<=1000
ORDER BY q.turn DESC LIMIT 1;
```

### Expected output

| turn | name |
| --- | --- |
| 3 | Cy |

### Interview follow up

If skipping people is allowed, why is this no longer a simple prefix problem?

Adapted problem with fresh data and explicit stop semantics. Source pattern: [LeetCode Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/).

## Q40 Reset running totals at reset events

**Pattern:** Prefix constraints and cumulative state

[Question and dataset](QUESTIONS.md#q40-reset-running-totals-at-reset-events)

```sql
WITH grouped AS (
  SELECT *,SUM(is_reset) OVER (ORDER BY seq ROWS UNBOUNDED PRECEDING) AS grp FROM events
)
SELECT seq,SUM(amount) OVER (PARTITION BY grp ORDER BY seq ROWS UNBOUNDED PRECEDING) AS running_total
FROM grouped ORDER BY seq;
```

### Why it works

A running count of reset events creates partitions. Each partition receives its own cumulative amount.

### The trap

Subtracting a global running minimum is unrelated to resets. Filtering reset rows before assigning groups removes the boundaries.

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

### Interview follow up

If a reset row also contains an amount, should that amount be included before or after the reset?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q41 Detect repeated values by row adjacency rather than ID arithmetic

**Pattern:** Gaps and islands

[Question and dataset](QUESTIONS.md#q41-detect-repeated-values-by-row-adjacency-rather-than-id-arithmetic)

```sql
WITH g AS (
  SELECT val,ROW_NUMBER() OVER (ORDER BY seq)
    -ROW_NUMBER() OVER (PARTITION BY val ORDER BY seq) AS island FROM logs
)
SELECT DISTINCT val FROM g WHERE val IS NOT NULL
GROUP BY val,island HAVING COUNT(*)>=3 ORDER BY val;
```

### Why it works

The difference between global and per-value row positions is constant within each uninterrupted value run. Group by both the value and the difference.

### The trap

Joining seq to seq+1 fails on sparse identifiers. Grouping by the difference alone can merge runs from different values.

### Alternative Three adjacent row positions using LEAD

```sql
WITH n AS (
  SELECT val,LEAD(val,1) OVER (ORDER BY seq) AS v1,
             LEAD(val,2) OVER (ORDER BY seq) AS v2 FROM logs
)
SELECT DISTINCT val FROM n WHERE val=v1 AND val=v2 ORDER BY val;
```

### Expected output

| val |
| --- |
| 7 |
| 8 |

### Interview follow up

If NULL itself is a meaningful repeated value, how should the query change?

Original extension distinguishing row adjacency from consecutive IDs. Pattern reference: [LeetCode Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/).

## Q42 Swap neighboring seats when seat IDs are sparse

**Pattern:** Positional pairing

[Question and dataset](QUESTIONS.md#q42-swap-neighboring-seats-when-seat-ids-are-sparse)

```sql
WITH positioned AS (
  SELECT *,ROW_NUMBER() OVER (ORDER BY seat_id) AS pos FROM seats
)
SELECT a.seat_id,COALESCE(b.occupant,a.occupant) AS occupant
FROM positioned a LEFT JOIN positioned b
  ON b.pos=CASE WHEN a.pos%2=1 THEN a.pos+1 ELSE a.pos-1 END
ORDER BY a.seat_id;
```

### Why it works

Pair ordinal positions, not numeric IDs. The unmatched last position falls back to its current occupant.

### The trap

seat_id +/- 1 and ID parity assume dense identifiers. A nullable occupant would require checking partner presence instead of COALESCE.

### Expected output

| seat_id | occupant |
| --- | --- |
| 10 | Ben |
| 20 | Ana |
| 40 | Di |
| 70 | Cy |
| 90 | Eli |

### Interview follow up

How would the logic differ for rotating groups of three instead of swapping pairs?

Original extension using position rather than ID parity. Pattern reference: [LeetCode Exchange Seats](https://leetcode.com/problems/exchange-seats/).

## Q43 Choose tournament winners when players occupy either match column

**Pattern:** Role unpivoting and tie rules

[Question and dataset](QUESTIONS.md#q43-choose-tournament-winners-when-players-occupy-either-match-column)

```sql
WITH points AS (
  SELECT first_player AS player_id,first_score AS score FROM matches
  UNION ALL SELECT second_player,second_score FROM matches
), totals AS (
  SELECT p.id,p.group_id,COALESCE(SUM(x.score),0) AS score
  FROM players p LEFT JOIN points x ON x.player_id=p.id GROUP BY p.id,p.group_id
), ranked AS (
  SELECT *,ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY score DESC,id) AS rn FROM totals
)
SELECT group_id,id AS winner_id,score FROM ranked WHERE rn=1 ORDER BY group_id;
```

### Why it works

Unpivot both participant roles before aggregation. Only after scores are complete does the stated tie rule select a winner.

### The trap

Joining only first_player misses half the contributions. UNION can erase two legitimate equal-scoring match contributions.

### Expected output

| group_id | winner_id | score |
| --- | --- | --- |
| 1 | 1 | 3 |
| 2 | 4 | 0 |

### Interview follow up

How would your result differ if the task asked for every tied winner?

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

## Q44 Compute cohort retention with a fixed signup denominator

**Pattern:** Grain and denominator traps

[Question and dataset](QUESTIONS.md#q44-compute-cohort-retention-with-a-fixed-signup-denominator)

```sql
SELECT u.signup_day,ROUND(AVG(CASE WHEN EXISTS (
  SELECT 1 FROM activity a WHERE a.user_id=u.id AND a.day_no=u.signup_day+1
) THEN 1.0 ELSE 0.0 END),2) AS retention
FROM users u GROUP BY u.signup_day ORDER BY u.signup_day;
```

### Why it works

Each signup contributes one indicator to the average. The source population is the cohort, not the people who happened to return.

### The trap

An inner join removes inactive users and repeated activity overweights active users. Consecutive activity days are not necessarily day-one retention.

### Expected output

| signup_day | retention |
| --- | --- |
| 1 | 0.33 |
| 2 | 1.0 |

### Interview follow up

For unfinished cohorts, how should the report exclude users whose day-one observation window has not closed?

Original practice exercise. Pattern reference: [SQLite SELECT and joins](https://www.sqlite.org/lang_select.html).

## Q45 Find consecutive over limit months across a year boundary

**Pattern:** Calendar adjacency and preaggregation

[Question and dataset](QUESTIONS.md#q45-find-consecutive-over-limit-months-across-a-year-boundary)

```sql
WITH monthly AS (
  SELECT c.account_id,c.month_index,SUM(c.amount) AS total
  FROM credits c GROUP BY c.account_id,c.month_index
), over_limit AS (
  SELECT m.* FROM monthly m JOIN accounts a ON a.id=m.account_id WHERE m.total>a.monthly_limit
), adjacent AS (
  SELECT *,LAG(month_index) OVER (PARTITION BY account_id ORDER BY month_index) AS prev FROM over_limit
)
SELECT DISTINCT account_id FROM adjacent WHERE month_index=prev+1 ORDER BY account_id;
```

### Why it works

Monthly aggregation precedes threshold testing. Month ordinals make year transitions and missing months explicit.

### The trap

Two over-limit observations can be separated by months. Comparing raw month numbers falsely treats December to January as a nonconsecutive transition.

### Expected output

| account_id |
| --- |
| 1 |

### Interview follow up

How would you derive month_index from actual dates in PostgreSQL or SQL Server?

Original practice exercise. Pattern reference: [SQLite Window Functions](https://sqlite.org/windowfunctions.html).

## Q46 Find all descendants without looping on cyclic relationships

**Pattern:** Recursive reachability

[Question and dataset](QUESTIONS.md#q46-find-all-descendants-without-looping-on-cyclic-relationships)

```sql
WITH RECURSIVE reachable(id) AS (
  SELECT 1
  UNION
  SELECT r.employee_id FROM reports r JOIN reachable x ON r.manager_id=x.id
)
SELECT id FROM reachable WHERE id<>1 ORDER BY id;
```

### Why it works

Deduplicate only the reachable identity. Every reachable ID can enter the state once, even through cycles and multiple paths.

### The trap

A fixed number of self joins assumes a maximum depth. UNION ALL with no visited-state guard keeps expanding the 1 to 2 to 3 to 1 cycle.

### Expected output

| id |
| --- |
| 2 |
| 3 |
| 4 |

### Interview follow up

If you must show each full reporting path, how will you prevent revisiting a node already in that path?

Original practice exercise. Pattern reference: [PostgreSQL Recursive Queries](https://www.postgresql.org/docs/current/queries-with.html).

## Q47 Classify tree nodes with root precedence

**Pattern:** Hierarchy classification

[Question and dataset](QUESTIONS.md#q47-classify-tree-nodes-with-root-precedence)

```sql
SELECT n.id,CASE
  WHEN n.parent_id IS NULL THEN 'Root'
  WHEN EXISTS (SELECT 1 FROM nodes c WHERE c.parent_id=n.id) THEN 'Inner'
  ELSE 'Leaf' END AS node_type
FROM nodes n ORDER BY n.id;
```

### Why it works

Test root status before child existence so the singleton root is classified correctly. EXISTS avoids expanding parents with multiple children.

### The trap

id NOT IN (SELECT parent_id ...) is poisoned by root NULLs. Checking leaf before root misclassifies a singleton.

### Expected output

| id | node_type |
| --- | --- |
| 1 | Root |
| 2 | Inner |
| 3 | Leaf |
| 4 | Leaf |
| 9 | Root |

### Interview follow up

How would you report orphan nodes whose non-null parent ID is missing from the master?

Adapted pattern with multiple rooted trees including a singleton. Source pattern: [LeetCode Tree Node](https://leetcode.com/problems/tree-node/).

## Q48 Find ordered funnel completions rather than mere event presence

**Pattern:** Ordered event matching

[Question and dataset](QUESTIONS.md#q48-find-ordered-funnel-completions-rather-than-mere-event-presence)

```sql
SELECT DISTINCT v.user_id FROM events v
WHERE v.kind='view' AND EXISTS (
  SELECT 1 FROM events a WHERE a.user_id=v.user_id AND a.kind='add' AND a.at>v.at
    AND EXISTS (
      SELECT 1 FROM events b WHERE b.user_id=a.user_id AND b.kind='buy' AND b.at>a.at
    )
) ORDER BY v.user_id;
```

### Why it works

Correlated existence checks preserve the ordering relation for a complete sequence. User 1 can use the later buy even though an earlier buy was out of order.

### The trap

COUNT(DISTINCT kind)=3 admits users 2 and 3. Taking only each kind first event can miss a valid later retry.

### Expected output

| user_id |
| --- |
| 1 |

### Interview follow up

How would you impose a maximum total funnel duration or require all steps within one session?

Original practice exercise. Pattern reference: [PostgreSQL Subquery Expressions](https://www.postgresql.org/docs/current/functions-subquery.html).

## Q49 Allocate supply to demand in FIFO order without a cursor

**Pattern:** Cumulative interval matching and FIFO

[Question and dataset](QUESTIONS.md#q49-allocate-supply-to-demand-in-fifo-order-without-a-cursor)

```sql
WITH s AS (
  SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM supplies
), d AS (
  SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM demands
)
SELECT d.id AS demand_id,s.id AS supply_id,
  CASE WHEN s.hi<d.hi THEN s.hi ELSE d.hi END
    -CASE WHEN s.hi-s.qty>d.hi-d.qty THEN s.hi-s.qty ELSE d.hi-d.qty END AS allocated
FROM s JOIN d ON s.hi>d.hi-d.qty AND d.hi>s.hi-s.qty
ORDER BY d.id,s.id;
```

### Why it works

Give supplies and demands half-open spans on a cumulative quantity axis. Their overlap length is the allocation, including partial splits.

### The trap

An equality join on cumulative endpoints misses split allocations. This formulation does not enforce receipt-before-demand time unless availability is separately guaranteed.

### Expected output

| demand_id | supply_id | allocated |
| --- | --- | --- |
| 1 | 1 | 5 |
| 1 | 2 | 2 |
| 2 | 2 | 2 |
| 2 | 3 | 3 |

### Interview follow up

How would you handle shortage, multiple products, or receipts arriving after a demand?

Adapted allocation pattern with fresh data. Source pattern: [Itzik Ben Gan Matching Supply With Demand Challenge](https://sqlperformance.com/2021/12/t-sql-queries/supply-demand-challenge).

## Q50 Value remaining FIFO inventory with a partially consumed batch

**Pattern:** Cumulative interval matching and FIFO

[Question and dataset](QUESTIONS.md#q50-value-remaining-fifo-inventory-with-a-partially-consumed-batch)

```sql
WITH incoming AS (
  SELECT *,SUM(qty) OVER (PARTITION BY product ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi
  FROM movements WHERE kind='IN'
), sold AS (
  SELECT product,SUM(CASE WHEN kind='OUT' THEN qty ELSE 0 END) AS qty
  FROM movements GROUP BY product
), leftovers AS (
  SELECT i.product,i.cost,CASE
    WHEN i.hi<=s.qty THEN 0
    WHEN i.hi-i.qty>=s.qty THEN i.qty
    ELSE i.hi-s.qty END AS remaining
  FROM incoming i JOIN sold s ON s.product=i.product
)
SELECT product,SUM(remaining) AS remaining_qty,SUM(remaining*cost) AS inventory_value
FROM leftovers GROUP BY product ORDER BY product;
```

### Why it works

Total sold consumes a prefix of each product cumulative receipt axis. Only the unconsumed suffix of each priced batch contributes value.

### The trap

Multiplying net quantity by an average or latest cost loses batch provenance. Fully consumed products must still return zero.

### Expected output

| product | remaining_qty | inventory_value |
| --- | --- | --- |
| A | 3 | 90 |
| B | 0 | 0 |

### Interview follow up

How should returned stock acquire its cost? What validation is needed before accepting negative stock histories?

Simplified adaptation with no returns or backorders. Source pattern: [Kathi Kellenberger FIFO Stock Inventory](https://www.red-gate.com/simple-talk/databases/sql-server/performance-sql-server/set-based-speed-phreakery-the-fifo-stock-inventory-sql-problem/).
