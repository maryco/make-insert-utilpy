import pandas as pd
from abc import ABCMeta, abstractmethod
from .constants import DEFINITIONS_MAP_POSTGRESQL, DEFINITIONS_MAP_MYSQL


class InsertBuilder(metaclass=ABCMeta):
    @abstractmethod
    def read_line(self, cmd: str, data: tuple) -> None:
        pass

    @abstractmethod
    def make_insert(self) -> None:
        pass

    @abstractmethod
    def _is_string_type(self, type: str) -> bool:
        pass

    def _transform(self, df_values: object, df_defs: object):
        _columns = []
        _values = []
        for column in df_defs.columns:
            df_colmn_def = df_defs.filter(items=[column])
            _value = self._make_value(
                getattr(df_values, column),
                df_colmn_def.loc['types'].values[0],
                df_colmn_def.loc['nullables'].values[0],
                df_colmn_def.loc['defaults'].values[0])
            if not _value is None:
                _columns.append(f"`{column}`")
                _values.append(_value)
        return _columns, _values

    def _make_value(self, value: any, type: str, nullable: str, default: any) -> any:
        if value == "%NONE%":
            return None

        if self._is_string_type(type):
            return f"'{value}'"
        else:
            return value

    def __repr__(self) -> str:
        return f"{self.table!r}\n\
          columns:{self.columns!r}\n\
            types:{self.col_types!r}\
            defaults:{self.defaults!r}\
            values:{self.values!r}"


class InsertForMySQL(InsertBuilder):

    def __init__(self, table: str, **kwargs) -> None:
        self.table = table
        self.defs = {}
        self._values = []

    def read_line(self, cmd: str, data: tuple) -> None:
        _cmd = cmd.lower()
        cmd_type = DEFINITIONS_MAP_MYSQL.get(_cmd)
        if (not cmd_type == None):
            self.defs[cmd_type] = data
        if _cmd == "value":
            self._values.append(data)

    def make_insert(self) -> None:
        if len(self._values) == 0:
            print(f"No insert data for {self.table}.")
            return

        df_defs = pd.DataFrame(data=[self.defs['types'],
                                     self.defs['nullables'],
                                     self.defs['defaults']],
                               columns=self.defs['columns'],
                               index=["types", "nullables", "defaults"])

        df_values = pd.DataFrame(
            data=self._values, columns=self.defs['columns'])

        for row in df_values.itertuples(name=self.table):
            _columns, _values = self._transform(row, df_defs)
            sql = f"INSERT INTO {self.table} ({', '.join(_columns)}) "
            sql += f"VALUES ({', '.join(_values)});"
            print(sql)

    def _is_string_type(self, type: str) -> bool:
        return not any(type.startswith(num_type)
                       for num_type in ["int", "bigint", "smallint", "tinyint", "float", "double"])


class InsertForPostgreSQL(InsertBuilder):

    def __init__(self, table: str, *, schema=None) -> None:
        self.table = table
        self.schema = schema
        self.defs = {}
        self._values = []

    def read_line(self, cmd: str, data: tuple) -> None:
        _cmd = cmd.lower()
        cmd_type = DEFINITIONS_MAP_POSTGRESQL.get(_cmd)
        if (not cmd_type == None):
            self.defs[cmd_type] = data
        if _cmd == "value":
            self._values.append(data)

    def make_insert(self) -> None:
        if len(self._values) == 0:
            print(f"No insert data for {self.table}.")
            return

        df_defs = pd.DataFrame(data=[self.defs['types'],
                                     self.defs['nullables'],
                                     self.defs['defaults']],
                               columns=self.defs['columns'],
                               index=["types", "nullables", "defaults"])

        overriding_phrase = " OVERRIDING SYSTEM VALUE" if df_defs.loc['defaults'].str.contains(
            "generated always as identity", case=False).sum() >= 1 else None

        df_values = pd.DataFrame(
            data=self._values, columns=self.defs['columns'])

        for row in df_values.itertuples(name=self.table):
            _columns, _values = self._transform(row, df_defs)
            sql = f"INSERT INTO {self._table_name()} ({', '.join(_columns)})"
            sql += f"{overriding_phrase} VALUES ({', '.join(_values)});"
            print(sql)

        if overriding_phrase is not None:
            # Update Sequence
            max_id = df_values['id'].max()
            if str(max_id).isdecimal():
                print(
                    f"SELECT SETVAL('{self._table_name()}_id_seq', {max_id});")

    def _is_string_type(self, type: str) -> bool:
        # TODO
        return not type in ("integer", "boolean", "smallint")

    def _table_name(self) -> str:
        if not self.schema is None:
            return f"{self.schema}.{self.table}"
        return self.table