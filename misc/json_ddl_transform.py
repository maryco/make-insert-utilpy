import json
import argparse
import sys

"""
Transform json to tsv.

> pipenv run python ./json_ddl_transform.py my.json

Transform json to sql for drawio imports.

> pipenv run python ./json_ddl_transform.py my.json --format sql
"""


def make_tsv(items, output_name):
    with open(f"../dist/{output_name}.tsv", "w") as fp_out:
        for item in items:
            # Column definition
            print(f'', file=fp_out)
            print(
                f"{item['tableComment']}\t{item['tableName']}", file=fp_out)
            for columns in extract_columns(item['columns']):
                print(f'{columns}', file=fp_out)

            # Index definition
            print(f'', file=fp_out)
            print(f'INDEX', file=fp_out)
            for constants in extract_constants(item['constants']):
                print(f'{constants}', file=fp_out)


def make_sql(items, output_name):
    with open(f"../dist/{output_name}.sql", "w") as fp_out:
        for item in items:
            # Column definition
            print(f'', file=fp_out)
            print(
                f"create table `{item['tableName']} {item['tableComment']}` (", file=fp_out)
            for columns in columns_to_create_sql(item['columns']):
                print(f'  {columns}', file=fp_out)
            print(f')', file=fp_out)


def columns_to_create_sql(items):
    rows = []
    list.sort(items, key=lambda x: x['position'])
    for column in items:
        row = [
            f"`{column['name']}`",
            column['type'],
            'PRIMARY KEY' if column['key'] == 'PRI' else '',
            ','
        ]
        rows.append(" ".join(map(str, row)))
    return rows


def extract_columns(items):
    rows = ["\t".join(['論理名', '物理名', '型', 'Null', 'Default', 'Key', '備考'])]
    list.sort(items, key=lambda x: x['position'])
    for column in items:
        row = [
            column['comment'],
            column['name'],
            column['type'],
            column['nullable'],
            column['default'],
            column['key'],
        ]
        rows.append("\t".join(map(str, row)))
    return rows


def extract_constants(items):
    rows = ["\t".join(['インデックス名', '', 'カラム', 'Unique'])]
    list.sort(items, key=lambda x: x['indexName'])
    for constant in items:
        row = [
            constant['indexName'],
            '',
            constant['column'],
            '' if constant['noUnique'] == 1 else 'YES'
        ]
        rows.append("\t".join(map(str, row)))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--format", default='tsv')
    args = parser.parse_args()

    json_file = f"{args.file}"
    format = args.format

    try:
        with open(json_file, "r") as fp_in:
            json_dict = json.load(fp_in)
            if format == 'sql':
                make_sql(json_dict, json_file)
            else:
                make_tsv(json_dict, json_file)
    except FileNotFoundError as e:
        sys.exit(f"File not found ({json_file}).")


if __name__ == "__main__":
    main()
