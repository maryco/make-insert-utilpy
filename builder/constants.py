DB_SUPPORTS = {
    "mysql": "InsertForMySQL", 
    "postgresql": "InsertForPostgreSQL"
}

DEFINITIONS_MAP_POSTGRESQL = {
    "column": "columns",
    "type": "types",
    "nullable": "nullables",
    "default": "defaults",
    "value": "values",
}

DEFINITIONS_MAP_MYSQL = {
    "column_name": "columns",
    "column_type": "types",
    "is_nullable": "nullables",
    "column_default": "defaults",
    "extra": "extra",
    "value": "values",
}
