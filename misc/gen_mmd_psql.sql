select '%%{init: { "theme": "neutral", "background": "#cccccc" } }%%'
union all
select 'erDiagram'
union all
select
    format(E'    %s {\n%s\n    }', 
        c.relname, 
        string_agg(format(E'        %s %s "%s"', 
            replace(format_type(t.oid, a.atttypmod), ' ', ''),
            a.attname,
            case when a.attname = 'id' then  obj_description(c.oid, 'pg_class') || 'の' || m.description else m.description end
        ), E'\n'))
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
group by c.relname
union all
select
    format('    %s }|--|| %s : %s', c1.relname, c2.relname, c.conname)
from
    pg_constraint c
    join pg_class c1 on c.conrelid = c1.oid and c.contype = 'f'
    join pg_class c2 on c.confrelid = c2.oid
where
    not c1.relispartition and not c2.relispartition;