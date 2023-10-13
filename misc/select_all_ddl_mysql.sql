select 
  table_name, column_name, column_type, is_nullable, column_key, column_default, extra
  from information_schema.columns
  where table_schema = 'some_db'
  order by table_name, ordinal_position
