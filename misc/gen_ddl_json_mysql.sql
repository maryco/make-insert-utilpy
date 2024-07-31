select JSON_ARRAYAGG(
	JSON_OBJECT(
		'tableName', table_name, 
		'tableComment', table_comment, 
		'columns', (
			select JSON_ARRAYAGG(
				JSON_OBJECT(
					'name', column_name,
					'type', column_type,
					'default', column_default,
					'nullable', is_nullable,
					'key', column_key,
					'comment', column_comment,
          'position', ordinal_position
				)
			) from information_schema.columns as cols
			where table_schema = 'somedb' and cols.table_name = tbls.table_name order by cols.ordinal_position
		),
		'constants', (
			select JSON_ARRAYAGG(
				JSON_OBJECT(
					'indexName', index_name,
					'column', column_name,
					'noUnique', non_unique
				)
			) from information_schema.statistics as sta
			where sta.table_schema = 'somedb' and sta.table_name = tbls.table_name
		)
	)
)
from information_schema.tables as tbls
  where table_schema = 'somedb' order by table_name;
