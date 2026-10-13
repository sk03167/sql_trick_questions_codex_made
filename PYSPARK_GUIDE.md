# PySpark companion guide

Every exercise Q01–Q50 now includes a PySpark DataFrame solution, executable sample setup and an explanation in [SOLUTIONS.md](SOLUTIONS.md). Question contracts and expected output are shared with [QUESTIONS.md](QUESTIONS.md). These are batch DataFrame exercises; they are not Structured Streaming implementations.

## Run locally

The reproducible baseline is **PySpark 4.0.1**, Java 17 and Python 3.13. Set JAVA_HOME to your Java 17 installation and use the same Python environment for the driver and workers. The pin is a tested baseline, not a claim that it is the newest release. [Apache installation requirements](https://spark.apache.org/docs/4.0.1/api/python/getting_started/install.html).

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-pyspark.txt
# On macOS with Java 17 installed:
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PYSPARK_PYTHON="$VIRTUAL_ENV/bin/python"
python pyspark_runner.py --question Q01
python verify_pyspark.py --question Q13
python verify_pyspark.py --report
```

Run commands from the repository root. On Linux/Windows, set JAVA_HOME to the installed JDK path using your shell's syntax; Windows also uses a different virtual-environment activation command. The runner creates one local Spark session, configures two worker threads, UTC and ANSI mode, and displays the selected answer. It deletes its temporary graph checkpoints only after consuming the result. None of these commands connects to a cloud workspace.

## Use a notebook or existing Spark session

Add this repository directory to the notebook's import path, or open the notebook with the repository root available. Reuse the runtime's existing `spark` session. Do not run local_session() to override a managed cluster. Set the SQL session timezone to your intended business timezone when replacing the integer time ordinals with real dates/timestamps.

```python
from pyspark_runner import load_tables
from pyspark_solutions import SOLUTIONS

t = load_tables(spark, 'Q13')
result = SOLUTIONS['Q13'](t)
result.show(truncate=False)
```

Each solution also prints its own explicit createDataFrame setup, so you can paste the input directly. Copy the displayed function plus its imports, or call the implementation in pyspark_solutions.py. The `t` dictionary maps each question's table names to DataFrames. Helpers below are shared by several questions. Q27 also reuses Q26.

The loader maps INTEGER to nullable LongType and TEXT to nullable StringType. Explicit schemas allow empty tables and columns containing only None. Spark does not enforce the fixture SQL PRIMARY KEY declarations: unique keys, positive interval lengths, valid forests and other assumptions remain input contracts. Treat NULL as Python None; NaN is a different value and is outside these fixtures.

## Execution and semantics

- Transformations are lazy. show, collect, checkpoint(eager=True) and emptiness checks can trigger execution. The solution functions do not collect business rows to Python; the verifier collects only tiny expected outputs for comparison.
- union/unionByName preserve duplicates. distinct removes whole-row duplicates. dropDuplicates(keys) does not define which remaining payload wins; use a deterministic ordered window when identity matters.
- Use explicit aliases for self joins. left_semi expresses existence and left_anti expresses absence while preserving left-side multiplicity. Ordinary equality does not match NULL keys; use eqNullSafe only when the question treats NULL as a value. [Join API](https://spark.apache.org/docs/4.0.1/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html), [null-safe equality](https://spark.apache.org/docs/3.5.6/api/python/reference/pyspark.sql/api/pyspark.sql.Column.eqNullSafe.html).
- ROWS counts physical positions in the specified ordering; RANGE groups value peers. An ordering alone normally uses a growing RANGE frame, so these functions make important frames explicit. Tie-break IDs are part of the logical contract. [Window frames](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Window.html).
- The ordered-window last operations in Q32/Q33 use full or prefix frames deliberately. Do not replace them with unordered group aggregates and expect stable last-row selection after a shuffle.
- Global windows deliberately serialize one logical sequence. At scale, partition by a genuine business key when the problem allows it; an arbitrary repartition cannot preserve a global order while removing that requirement.
- Joins and groupings can shuffle. Inspect result.explain('formatted'), actual cardinalities and skew before tuning. Broadcasting is appropriate only when measured input size fits worker memory. The two-shuffle-partition local setting is for these tiny fixtures.
- Q19 generates a Cartesian nearest-match candidate set. Q26 creates a requirement grid. Q28 builds exact arrays per basket. Q49 uses interval overlap joins. These teach correctness and have explicit scale limits; they are not performance benchmarks.
- Day/minute/month integers retain the SQL question conventions. They are not YYYYMMDD values. LongType arithmetic can overflow; production money/counts may need DecimalType and a declared precision/rounding policy. Approximate distinct counts or quantiles would change exact answers.

## Graph iteration and checkpoints

Q05 and Q46 use iterative DataFrame joins instead of requiring recursive SQL support. The helper expands a frontier and anti joins the already-seen keys. A finite graph eventually has no new pairs, so duplicate edges and cycles cannot keep it running. Q05 retains an all-pairs closure, which can be expensive for large components.

The helper uses durable DataFrame checkpointing to truncate growing logical plans. Configure a writable checkpoint directory BEFORE calling it. For a local notebook:

```python
import tempfile
from pyspark_runner import load_tables
from pyspark_solutions import q05

with tempfile.TemporaryDirectory(prefix='graph-checkpoints-') as directory:
    spark.sparkContext.setCheckpointDir(directory)
    answer = q05(load_tables(spark, 'Q05'))
    answer.show(truncate=False)  # Consume before the context removes checkpoints.
```

On a distributed cluster use a unique, cluster-accessible supported filesystem path instead of a driver-local temporary directory. Keep it until all dependent actions finish, then clean it up according to your job lifecycle. These examples were verified with classic Spark; their sparkContext checkpoint setup is not a Spark Connect recipe. [Checkpoint API](https://spark.apache.org/docs/4.0.1/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.checkpoint.html).

## Shared helper implementations

The following code is extracted from the same source executed by the tests.

```python
def prefix(window):
    return window.rowsBetween(Window.unboundedPreceding, Window.currentRow)
```

```python
def pack_intervals(df, start='start_at', end='end_at'):
    """Pack touching/overlapping positive-length intervals, including nesting."""
    w = Window.orderBy(start, end, 'id')
    marked = df.withColumn('_previous_max', F.max(end).over(
        w.rowsBetween(Window.unboundedPreceding, -1)))
    marked = marked.withColumn('_fresh', F.when(
        F.col('_previous_max').isNull() | (F.col(start) > F.col('_previous_max')), 1).otherwise(0))
    grouped = marked.withColumn('_island', F.sum('_fresh').over(prefix(w)))
    return grouped.groupBy('_island').agg(
        F.min(start).alias(start), F.max(end).alias(end)).drop('_island')
```

```python
def reachability(seeds, edges):
    """Distinct (root,node) closure; requires a configured checkpoint directory.

    seeds: root,node. edges: src,dst. No graph rows are collected to Python.
    Durable checkpoints bound plan growth; the caller owns their cleanup.
    """
    seen = seeds.distinct().checkpoint(eager=True)
    frontier = seen
    edges = edges.distinct()
    while True:
        candidates = (frontier.alias('f').join(edges.alias('e'),
            F.col('f.node') == F.col('e.src'))
            .select('f.root', F.col('e.dst').alias('node')).distinct())
        fresh = candidates.join(seen, ['root', 'node'], 'left_anti').checkpoint(eager=True)
        if fresh.isEmpty():
            return seen
        seen = seen.unionByName(fresh).checkpoint(eager=True)
        frontier = fresh
```

## Question index

| ID | PySpark solution | Pattern |
| --- | --- | --- |
| Q01 | [Deduplicate reverse routes while preserving an original row](SOLUTIONS.md#pyspark-q01) | Unordered pairs and symmetry breaking |
| Q02 | [Find reciprocal pairs without matching a row to itself](SOLUTIONS.md#pyspark-q02) | Unordered pairs and symmetry breaking |
| Q03 | [Count undirected neighbors despite duplicated edge directions](SOLUTIONS.md#pyspark-q03) | Graph edge normalization |
| Q04 | [Find graph triangles exactly once](SOLUTIONS.md#pyspark-q04) | Graph edge normalization |
| Q05 | [Assign connected components including isolated nodes](SOLUTIONS.md#pyspark-q05) | Recursive reachability |
| Q06 | [Compress integer sequences with duplicate input values](SOLUTIONS.md#pyspark-q06) | Gaps and islands |
| Q07 | [Find every longest login streak with duplicate logins](SOLUTIONS.md#pyspark-q07) | Gaps and islands |
| Q08 | [Find missing ranges including the boundaries](SOLUTIONS.md#pyspark-q08) | Gaps and islands |
| Q09 | [Sessionize events with an exact inactivity threshold](SOLUTIONS.md#pyspark-q09) | Sessionization and change points |
| Q10 | [Group status runs with NULL states and missing days](SOLUTIONS.md#pyspark-q10) | Sessionization and change points |
| Q11 | [Return every row in qualifying ID streaks](SOLUTIONS.md#pyspark-q11) | Gaps and islands |
| Q12 | [Reconstruct projects from one day tasks](SOLUTIONS.md#pyspark-q12) | Gaps and islands |
| Q13 | [Merge overlapping intervals even when they are nested](SOLUTIONS.md#pyspark-q13) | Interval packing and sweep lines |
| Q14 | [Find free time between overlapping bookings](SOLUTIONS.md#pyspark-q14) | Interval packing and sweep lines |
| Q15 | [Find peak simultaneous meetings with tied event times](SOLUTIONS.md#pyspark-q15) | Interval packing and sweep lines |
| Q16 | [Measure occupied duration without counting overlaps twice](SOLUTIONS.md#pyspark-q16) | Interval packing and sweep lines |
| Q17 | [Resolve prices as of a date while keeping products without history](SOLUTIONS.md#pyspark-q17) | Temporal and nearest joins |
| Q18 | [Join facts to effective dated dimensions at a shared boundary](SOLUTIONS.md#pyspark-q18) | Temporal and nearest joins |
| Q19 | [Choose the closest observation with a deterministic tie rule](SOLUTIONS.md#pyspark-q19) | Temporal and nearest joins |
| Q20 | [Find nonbuyers when the purchase table contains NULL](SOLUTIONS.md#pyspark-q20) | NULL semantics and anti joins |
| Q21 | [Keep parents that have no qualifying child rows](SOLUTIONS.md#pyspark-q21) | NULL semantics and anti joins |
| Q22 | [Aggregate orders and payments without join fan out](SOLUTIONS.md#pyspark-q22) | Join grain and multiplicity |
| Q23 | [Preserve independent transaction amounts when duplicate values are valid](SOLUTIONS.md#pyspark-q23) | Join grain and multiplicity |
| Q24 | [Reconcile two snapshots including NULL valued changes](SOLUTIONS.md#pyspark-q24) | Set and multiset reconciliation |
| Q25 | [Reconcile duplicate counts rather than just distinct rows](SOLUTIONS.md#pyspark-q25) | Set and multiset reconciliation |
| Q26 | [Find customers covering every required product](SOLUTIONS.md#pyspark-q26) | Relational division and set equality |
| Q27 | [Find customers whose basket exactly equals the required set](SOLUTIONS.md#pyspark-q27) | Relational division and set equality |
| Q28 | [Find pairs of customers with identical baskets including empty ones](SOLUTIONS.md#pyspark-q28) | Relational division and set equality |
| Q29 | [Find students who never scored an exam extreme](SOLUTIONS.md#pyspark-q29) | Universal conditions and exclusion |
| Q30 | [Combine duplicate and unique conditions at different grains](SOLUTIONS.md#pyspark-q30) | Independent grouping grains |
| Q31 | [Explain peer expansion in ROWS versus RANGE](SOLUTIONS.md#pyspark-q31) | Window frames and peer rows |
| Q32 | [Get the true last value rather than the last value so far](SOLUTIONS.md#pyspark-q32) | Window frames and peer rows |
| Q33 | [Forward fill NULLs even when values decrease](SOLUTIONS.md#pyspark-q33) | Window frames and missing values |
| Q34 | [Compute a calendar rolling average with missing days](SOLUTIONS.md#pyspark-q34) | Calendar completion and rolling windows |
| Q35 | [Count distinct active users across a rolling calendar window](SOLUTIONS.md#pyspark-q35) | Calendar completion and rolling windows |
| Q36 | [Maintain a cumulative distinct count without a distinct window aggregate](SOLUTIONS.md#pyspark-q36) | Window frames and missing values |
| Q37 | [Compute group medians without losing duplicate observations](SOLUTIONS.md#pyspark-q37) | Order statistics and weighted distributions |
| Q38 | [Find the median from value frequencies without expanding rows](SOLUTIONS.md#pyspark-q38) | Order statistics and weighted distributions |
| Q39 | [Find the last person in a capacity limited boarding prefix](SOLUTIONS.md#pyspark-q39) | Prefix constraints and cumulative state |
| Q40 | [Reset running totals at reset events](SOLUTIONS.md#pyspark-q40) | Prefix constraints and cumulative state |
| Q41 | [Detect repeated values by row adjacency rather than ID arithmetic](SOLUTIONS.md#pyspark-q41) | Gaps and islands |
| Q42 | [Swap neighboring seats when seat IDs are sparse](SOLUTIONS.md#pyspark-q42) | Positional pairing |
| Q43 | [Choose tournament winners when players occupy either match column](SOLUTIONS.md#pyspark-q43) | Role unpivoting and tie rules |
| Q44 | [Compute cohort retention with a fixed signup denominator](SOLUTIONS.md#pyspark-q44) | Grain and denominator traps |
| Q45 | [Find consecutive over limit months across a year boundary](SOLUTIONS.md#pyspark-q45) | Calendar adjacency and preaggregation |
| Q46 | [Find all descendants without looping on cyclic relationships](SOLUTIONS.md#pyspark-q46) | Recursive reachability |
| Q47 | [Classify tree nodes with root precedence](SOLUTIONS.md#pyspark-q47) | Hierarchy classification |
| Q48 | [Find ordered funnel completions rather than mere event presence](SOLUTIONS.md#pyspark-q48) | Ordered event matching |
| Q49 | [Allocate supply to demand in FIFO order without a cursor](SOLUTIONS.md#pyspark-q49) | Cumulative interval matching and FIFO |
| Q50 | [Value remaining FIFO inventory with a partially consumed batch](SOLUTIONS.md#pyspark-q50) | Cumulative interval matching and FIFO |

## Maintaining and testing the catalogue

Edit pyspark_solutions.py and pyspark_notes.json, then run `python build_catalog.py`. The generator copies the exact function source into SOLUTIONS.md and writes the helper guide; it does not require PySpark to be installed. The sample DataFrames are generated from catalog.json's source questions in build_catalog.py, keeping SQL and Python fixtures aligned.

Run `python validate_pyspark_docs.py` to check every embedded Python section, fixture setup, helper and internal link. Run the Spark verifier for executable behavior; docs checks alone cannot establish correctness. [Recorded PySpark checks](PYSPARK_VERIFICATION.md) and [SQL checks](VERIFICATION.md) describe their separate scopes. The GitHub workflow runs both engines and checks generated-document consistency.
