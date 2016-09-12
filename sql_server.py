import pyodbc
from properties import get_property

CON_STRING = get_property('properties.json', 'connection_string')


def connect():
    connection = pyodbc.connect(CON_STRING)

    return connection


if __name__ == '__main__':
    result = connect()

    print result