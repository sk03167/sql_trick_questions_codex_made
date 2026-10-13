"""Load the catalogue's fixtures with explicit Spark schemas and run one exercise."""
import argparse
import json
import os
from pathlib import Path
import random
import tempfile

from pyspark.sql import SparkSession, types as T
from pyspark_solutions import SOLUTIONS

ROOT = Path(__file__).resolve().parent
CATALOG = {q['id']: q for q in json.loads((ROOT / 'catalog.json').read_text())}


def load_tables(spark, question, replacements=None, shuffle=False):
    tables = {}
    rng = random.Random(317)
    for table in CATALOG[question]['tables']:
        fields = []
        for name, sql_type in table['columns']:
            if sql_type.startswith('INTEGER'):
                kind = T.LongType()
            elif sql_type.startswith('TEXT'):
                kind = T.StringType()
            else:
                raise ValueError(f'Add an explicit mapping for {sql_type}')
            fields.append(T.StructField(name, kind, nullable=True))
        rows = list((replacements or {}).get(table['name'], table['rows']))
        if shuffle:
            rng.shuffle(rows)
        df = spark.createDataFrame(rows, T.StructType(fields))
        tables[table['name']] = df.repartition(3) if shuffle else df
    return tables


def local_session():
    # Resource limits suit tiny interview fixtures, not production sizing.
    os.environ.setdefault('SPARK_LOCAL_IP', '127.0.0.1')
    return (SparkSession.builder.master('local[2]').appName('sql-pyspark-catalog')
            .config('spark.ui.enabled', 'false').config('spark.sql.shuffle.partitions', '2')
            .config('spark.sql.session.timeZone', 'UTC').config('spark.sql.ansi.enabled', 'true')
            .config('spark.ui.showConsoleProgress', 'false').getOrCreate())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--question', choices=sorted(CATALOG), required=True)
    args = parser.parse_args()
    spark = local_session()
    spark.sparkContext.setLogLevel('ERROR')
    try:
        with tempfile.TemporaryDirectory(prefix='sql-pyspark-checkpoints-') as directory:
            spark.sparkContext.setCheckpointDir(directory)
            result = SOLUTIONS[args.question](load_tables(spark, args.question))
            result.show(truncate=False)
    finally:
        spark.stop()


if __name__ == '__main__':
    main()
