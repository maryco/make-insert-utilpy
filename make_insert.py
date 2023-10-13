import sys
import argparse
import pandas as pd
from builder import *

"""
(e.g) Create insert sql for PostgreSQL. (default)
> pipenv run python ./make_insert.py --input ./resources_psql/sample_client.tsv --schema myschema

(e.g) Create sql for MySQL.
> pipenv run python ./make_insert.py --input ./resources_mysql/sample_access_logs.tsv --dbtype mysql > ./dist/access_logs_test.sql
"""


def main():
    parser = argparse.ArgumentParser(description="Create insert sql from tsv.")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument(
        "--dbtype", type=str, default="postgresql", choices=DB_SUPPORTS.keys())
    parser.add_argument("--schema", default=None, type=str)
    args = parser.parse_args()

    resource_path = args.input

    try:
        with open(resource_path, "r") as fp:
            base_df = pd.read_table(resource_path, header=None,
                                    encoding="utf-8", index_col=0)
    except FileNotFoundError as e:
        sys.exit(f"Not found resource file ({resource_path}).")

    df = base_df.groupby(0, group_keys=False).apply(
        lambda x: x).fillna("%NONE%")

    cls = globals()[DB_SUPPORTS.get(args.dbtype)]
    builder = cls(table=df.index.unique()[0], schema=args.schema)

    for row in df.rename(columns={1: "command"}).itertuples():
        # print(f"{row.Index} = {row.command}")
        # print(row)
        builder.read_line(row.command, row[2:])

    builder.make_insert()


if __name__ == "__main__":
    main()
