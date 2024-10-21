import os
import cx_Oracle as cxo
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateTable
from langchain_community.utilities.sql_database import SQLDatabase
import config
from urllib.parse import quote

username = config.db['user']
password = quote(config.db['secret'])
host = config.db['host']
port = config.db['port']
mydatabase = config.db['database']

oracle_connection_string_fmt = (
    'oracle+cx_oracle://{username}:{password}@' +
    cxo.makedsn(host, port, service_name=mydatabase)
)
url = oracle_connection_string_fmt.format(
    username=username, password=password, hostname=host, port=port, service_name=mydatabase
)

engine = create_engine(url, echo=True)
metadata = MetaData()
metadata.reflect(bind=engine)

# Extract and print schema
schema_dump = ""
for table in metadata.sorted_tables:
    create_table_statement = str(CreateTable(table).compile(dialect=engine.dialect))
    schema_dump += create_table_statement + ';\n\n'
    if table.comment:
        schema_dump += f'COMMENT ON TABLE {table.name} IS \'{table.comment}\';\n\n'
    for column in table.columns:
        if column.comment:
            schema_dump += f'COMMENT ON COLUMN {table.name}.{column.name} IS \'{column.comment}\';\n'

db = SQLDatabase(engine)
