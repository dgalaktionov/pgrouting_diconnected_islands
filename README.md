# pgrouting_diconnected_islands
A script to remove disconnected islands in a pgrouting network

## Requires:
Python 2
networkx and psycopg2

Both are available as pip packages.

## Usage:
python islands.py $DATABASE_NAME $TABLE_NAME [user=postgres] [password=postgres] [host=localhost] [port=5432]

Arguments in brackets [] are optional.
