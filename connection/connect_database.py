import sqlite3
from sqlite3 import Connection, Error


def connect_database(db_file: str) -> Connection | None:
  conn = None
  try:
    conn = sqlite3.connect(db_file)
    # print(sqlite3.version_info)
  except Error as err:
    print(f"Error: {err}")

  return conn
