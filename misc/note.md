
## make_insert.py

https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

## make_template_header.py

- https://pandas.pydata.org/docs/user_guide/groupby.html#iterating-through-groups
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
- Pandas 行と列の入れ替え、縦持ち横持ち変換
  - https://python.always-basics.com/python/pandas/pandas-transpose/

## TIPS: 

MySQL logging cli 

> \T ./output.txt
>> Logging to file './output.txt'

MySQL execute from file and result to file

> --batch, -B ...カラム区切り文字としてタブを使用し、各行を新しい行に出力します
> --execute, -e ...SQL実行

> mysql {connect to target db options} -B < select_all_ddl_mysql.sql > my_local_db_all_ddl.sql.tsv

```sql
select 
  TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
  from information_schema.columns
  where TABLE_SCHEMA = 'my_local_db'
  order by TABLE_NAME, ORDINAL_POSITION
```

- INFORMATION_SCHEMA COLUMNS テーブル
https://dev.mysql.com/doc/refman/8.0/ja/information-schema-columns-table.html

