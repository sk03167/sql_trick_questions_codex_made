"""Execute DataFrame solutions against independent expected rows and edge oracles."""
import argparse
from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import platform
import sqlite3
import tempfile

import verify as sql_checks
from pyspark_runner import CATALOG, load_tables, local_session
from pyspark_solutions import SOLUTIONS, q01_left_join

ROOT = Path(__file__).resolve().parent


def compare(actual, expected):
    assert len(actual) == len(expected), (actual, expected)
    for row, want in zip(actual, expected):
        assert len(row) == len(want), (row, want)
        for got, value in zip(row, want):
            if isinstance(value, float):
                assert got is not None and math.isclose(float(got), value, rel_tol=1e-10, abs_tol=1e-10), (row, want)
            else:
                assert got == value, (row, want)


def expected_columns(qid):
    with sqlite3.connect(':memory:') as db:
        db.executescript((ROOT / 'sql' / f'{qid}_setup.sql').read_text())
        cursor = db.execute(CATALOG[qid]['sql'])
        return [column[0] for column in cursor.description]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--question', choices=sorted(CATALOG))
    p.add_argument('--random-cases', type=int, default=3)
    p.add_argument('--skip-shuffle', action='store_true')
    p.add_argument('--report', action='store_true', help='Write report only for a complete default suite')
    args = p.parse_args()
    if args.random_cases < 0:
        p.error('--random-cases must be nonnegative')
    if args.report and (args.question or args.skip_shuffle or args.random_cases != 3):
        p.error('--report requires the complete default suite')
    selected = {args.question} if args.question else set(CATALOG)
    counters = Counter()
    spark = local_session()
    spark.sparkContext.setLogLevel('ERROR')
    try:
        with tempfile.TemporaryDirectory(prefix='sql-pyspark-tests-') as directory:
            spark.sparkContext.setCheckpointDir(directory)

            def check(qid, expected, replacements=None, family='samples', alternatives=False, shuffle=False):
                tables = load_tables(spark, qid, replacements, shuffle=shuffle)
                answer = SOLUTIONS[qid](tables)
                assert answer.columns == expected_columns(qid), (qid, answer.columns)
                try:
                    compare([tuple(row) for row in answer.collect()], expected)
                    if qid == 'Q01':
                        compare([tuple(row) for row in q01_left_join(tables).collect()], expected)
                        counters['Q01 left-join alternative'] += 1
                except AssertionError as exc:
                    raise AssertionError(f'{qid}: {family}, replacements={replacements}: {exc}') from exc
                counters[family] += 1
                print(f'PASS {qid}: {family}', flush=True)

            for qid in sorted(selected):
                check(qid, CATALOG[qid]['expected'])
            # Reuse the independent Python oracles; do not use SQLite output as expected rows.
            original = sql_checks.check
            try:
                sql_checks.check = check
                sql_checks.explicit_edges(selected)
                sql_checks.randomized(selected, cases=args.random_cases)
            finally:
                sql_checks.check = original
            extra = [
                ('Q05', {'nodes': [], 'edges': []}, []),
                ('Q15', {'meetings': []}, []),
                ('Q25', {'old_bag': [(None,), (None,)], 'new_bag': [(None,)]}, [(None, -1)]),
                ('Q31', {'tx': [(2, 1, 7), (1, 1, 5)]}, [(1, 5, 12), (2, 12, 12)]),
                ('Q32', {'events': [(1, 1, 0, 9), (2, 1, 1, None)]}, [(1, None), (2, None)]),
                ('Q33', {'readings': [(1, 1, 1, 9), (2, 1, 2, -4), (3, 1, 3, None)]}, [(1, 9), (2, -4), (3, -4)]),
                ('Q34', {'sales': []}, [(3, 0, 0.0), (4, 0, 0.0), (5, 0, 0.0)]),
                ('Q38', {'frequencies': [(2, 1), (9, 1)]}, [(5.5,)]),
                ('Q38', {'frequencies': [(1, 4503599627370496), (9, 4503599627370497)]}, [(9.0,)]),
                ('Q42', {'seats': [(100, 'alone')]}, [(100, 'alone')]),
                ('Q48', {'events': [(1, 1, 'add', 1), (2, 1, 'view', 2), (3, 1, 'add', 3), (4, 1, 'buy', 4),
                                      (5, 2, 'view', 1), (6, 2, 'add', 1), (7, 2, 'buy', 2)]}, [(1,)]),
                ('Q49', {'supplies': [(1, 4), (2, 6)], 'demands': [(1, 4), (2, 6)]}, [(1, 1, 4), (2, 2, 6)]),
            ]
            for qid, replacements, expected in extra:
                if qid in selected:
                    check(qid, expected, replacements, 'PySpark targeted edges')
            if not args.skip_shuffle:
                for qid in sorted(selected):
                    check(qid, CATALOG[qid]['expected'], family='shuffled inputs across 3 partitions', shuffle=True)
            total = sum(counters.values())
            print(f'PASS: {len(selected)} exercises; {total} DataFrame result checks; Spark {spark.version}', flush=True)
            if args.report:
                details = '\n'.join(f'| {name} | {n} |' for name, n in counters.items())
                report = f'''# PySpark verification

Verified {date.today().isoformat()} with PySpark {spark.version}, Python {platform.python_version()}, Java {spark.sparkContext._jvm.java.lang.System.getProperty('java.version')}, local[2], ANSI mode enabled and UTC session time zone.

All **{total} DataFrame result checks passed** across all 50 exercises. Output column names, row order, NULL values and multiplicities are checked, with a 1e-10 tolerance for floating-point results. The Q01 left-join alternative is also executed.

| Check family | Passed |
| --- | --- |
{details}

Every original fixture is tested again after shuffling its input rows and repartitioning each input to three partitions. Explicit edge cases are imported from the SQL verifier. Its independent Python graph, interval, set, median and FIFO oracles generate three fixtures per randomized family using seed 20261010. Additional tests cover null final values, decreasing forward fills, empty calendars/graphs, exact FIFO boundaries and a funnel with an invalid early attempt followed by a valid one.

Reproduce with `python verify_pyspark.py --report`. Run `python verify.py` separately for the larger SQLite suite. Spark tests execute the DataFrame API, not the SQLite SQL strings. Only tiny fixtures are collected for assertion. Cluster scaling, Spark Connect, managed cloud runtimes and other Spark versions are not covered by this local run.
'''
                (ROOT / 'PYSPARK_VERIFICATION.md').write_text(report)
    finally:
        spark.stop()


if __name__ == '__main__':
    main()
