"""Render PySpark sections from executable source; no Spark installation required."""
import ast
import json
from pathlib import Path
import pprint

ROOT = Path(__file__).resolve().parent


def sources():
    text = (ROOT / 'pyspark_solutions.py').read_text()
    return {node.name: ast.get_source_segment(text, node) for node in ast.parse(text).body
            if isinstance(node, ast.FunctionDef)}


def question_section(q):
    ident = q['id']
    return f'[SQL solution](SOLUTIONS.md#{ident.lower()}-{q["title"].lower().replace(" ", "-")}) · [PySpark solution](SOLUTIONS.md#pyspark-{ident.lower()})'


def solution_section(q):
    src = sources()
    ident, fn = q['id'], q['id'].lower()
    notes = json.loads((ROOT / 'pyspark_notes.json').read_text())
    imports = 'from pyspark.sql import Window, functions as F\n'
    needed = [name for name in ['prefix', 'pack_intervals', 'reachability']
              if any(isinstance(node, ast.Name) and node.id == name for node in ast.walk(ast.parse(src[fn])))]
    if needed:
        imports += 'from pyspark_solutions import ' + ', '.join(needed) + '\n'
    if ident == 'Q27':
        imports += 'from pyspark_solutions import q26\n'
    setup = ['t = {}']
    for table in q['tables']:
        schema = ', '.join(name + (' long' if kind.startswith('INTEGER') else ' string') for name, kind in table['columns'])
        rows = pprint.pformat([tuple(row) for row in table['rows']], width=88)
        setup.append(f't[{table["name"]!r}] = spark.createDataFrame(\n    {rows},\n    {schema!r}\n)')
    parts = [f'### PySpark {ident}',
             'Use an existing `spark` session and the repository on your Python import path. '
             '[Setup, shared helpers, and runtime notes](PYSPARK_GUIDE.md). The output matches the expected table below.',
             '**Create the sample DataFrames**', '```python\n' + '\n'.join(setup) + '\n```',
             '**DataFrame solution**', '```python\n' + imports + '\n' + src[fn] + f'\n\nresult = {fn}(t)\nresult.show(truncate=False)\n```',
             '**How it works and what to watch:** ' + notes[ident]]
    if ident in {'Q05', 'Q46'}:
        parts.insert(2, '**Before running:** configure a checkpoint directory as shown in '
                     '[graph iteration setup](PYSPARK_GUIDE.md#graph-iteration-and-checkpoints). The local runner handles this automatically.')
    if ident == 'Q01':
        parts.extend(['**Alternative: left join and keep unmatched rows**', '```python\n' + src['q01_left_join'] + '\n\nq01_left_join(t).show(truncate=False)\n```'])
    return parts


def write_guide(questions):
    src = sources()
    intro = '''# PySpark companion guide

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
'''
    helpers = '\n\n'.join('```python\n' + src[name] + '\n```' for name in ['prefix', 'pack_intervals', 'reachability'])
    index = '\n'.join(f'| {q["id"]} | [{q["title"]}](SOLUTIONS.md#pyspark-{q["id"].lower()}) | {q["pattern"]} |' for q in questions)
    end = '''

## Maintaining and testing the catalogue

Edit pyspark_solutions.py and pyspark_notes.json, then run `python build_catalog.py`. The generator copies the exact function source into SOLUTIONS.md and writes the helper guide; it does not require PySpark to be installed. The sample DataFrames are generated from catalog.json's source questions in build_catalog.py, keeping SQL and Python fixtures aligned.

Run `python validate_pyspark_docs.py` to check every embedded Python section, fixture setup, helper and internal link. Run the Spark verifier for executable behavior; docs checks alone cannot establish correctness. [Recorded PySpark checks](PYSPARK_VERIFICATION.md) and [SQL checks](VERIFICATION.md) describe their separate scopes. The GitHub workflow runs both engines and checks generated-document consistency.
'''
    (ROOT / 'PYSPARK_GUIDE.md').write_text(intro + '\n' + helpers + '\n\n## Question index\n\n| ID | PySpark solution | Pattern |\n| --- | --- | --- |\n' + index + end)
