import sys
import csv
from pathlib import Path
import pandas as pd

"""
1. Get all table definitions from target database.

> mysql {connect to target db options} -B < select_all_ddl_mysql.sql > all_ddl.tsv

```sql
select 
  TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
  from information_schema.columns
  where TABLE_SCHEMA = 'some_db'
  order by TABLE_NAME, ORDINAL_POSITION
```

2. Make test data template headers for all tables.

> pipenv run python ./make_template_header.py all_ddl.tsv test_data_templates.tsv
"""


def main():
    if (len(sys.argv) != 3):
        sys.exit(f"Required input and output tsv file.")

    resource_file = f"{sys.argv[1]}"
    output_file = f"./dist/{sys.argv[2]}"

    headers = ["TABLE_NAME", "COLUMN_NAME", "COLUMN_TYPE",
               "IS_NULLABLE", "COLUMN_KEY", "COLUMN_DEFAULT", "EXTRA"]
    dtypes = {"TABLE_NAME": str, "COLUMN_NAME": str, "COLUMN_TYPE": str,
              "IS_NULLABLE": str, "COLUMN_KEY": str, "COLUMN_DEFAULT": str, "EXTRA": str}
    try:
        with open(resource_file, "r") as fp:
            df = pd.read_table(resource_file, header=0,
                               names=headers, dtype=dtypes,
                               encoding="utf-8", index_col=0)
    except FileNotFoundError as e:
        sys.exit(f"Not found resource file ({resource_file}).")

    output = Path(output_file)
    if (output.exists()):
        output.unlink()

    with open(output, "a+", newline='') as fp:
        _writer = csv.writer(fp, delimiter="\t",
                             dialect="unix", quoting=csv.QUOTE_MINIMAL)
        for name, group in df.groupby("TABLE_NAME"):
            # テーブル名を削除して転置
            df_of_table = pd.DataFrame(group, columns=headers).fillna("")
            df_of_table.drop(axis=0, columns=["TABLE_NAME"], inplace=True)
            df_of_table = df_of_table.T
            # DataFrameだと扱いづらいので先頭にテーブル名を追加したListから出力
            # print(f"{df_of_table!r}")
            # df_of_table.to_csv(output_file, header=None, sep="\t", mode="a+")
            for row in df_of_table.itertuples():
                raw_list = list(row)
                raw_list.insert(0, name)
                _writer.writerow(raw_list)


if __name__ == "__main__":
    main()
