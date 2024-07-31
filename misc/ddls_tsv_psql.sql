select
    format(E'%s\t%s\t%s\t%s\t%s',
        c.relname,
        obj_description(c.oid, 'pg_class'),
        a.attname,
        format_type(t.oid, a.atttypmod),
        m.description
    )
from
    pg_class c 
    join pg_namespace n on n.oid = c.relnamespace
    left join pg_attribute a ON c.oid = a.attrelid and a.attnum > 0 and not a.attisdropped
    left join pg_type t ON a.atttypid = t.oid
    left join pg_description m ON a.attnum = m.objsubid AND a.attrelid = m.objoid
where
    c.relkind in ('r', 'p') 
    and not c.relispartition
    and n.nspname !~ '^pg_' AND n.nspname <> 'information_schema'
order by c.relname, a.attname, format_type(t.oid, a.atttypmod)
