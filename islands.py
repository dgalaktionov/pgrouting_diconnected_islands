#!/usr/bin/python

import networkx as nx
import psycopg2
import sys


def get_first_island(connected_components, N):
	nums = [nx.number_of_edges(g) for g in connected_components]
	first_island = None

	if len(nums) > 1:
		if nums[1]/N > 0.1:
			sys.stderr.write("WARNING: Second largest group contains %2.2f %% of edges.\n" % (100*nums[1]/N))

		try:
			first_island = (i for i,v in enumerate(nums) if v/N <= 0.1).next()
		except StopIteration:
			pass

	return first_island



argv = sys.argv

if len(argv) < 3:
	print "Usage: python islands.py $DATABASE_NAME $TABLE_NAME [user=postgres] [password=postgres] [host=localhost] [port=5432]"
	print "Arguments in brackets [] are optional"
	sys.exit(1)

dbname = argv[1]
table = argv[2]
parameters = {}

if len(argv) > 3:
	splitted = [arg.split("=") for arg in argv[3:]]
	parameters = dict([(split[0], split[1]) for split in splitted if len(split) == 2])

parameters["database"] = dbname

if "user" not in parameters:
	parameters["user"] = "postgres"
	parameters["password"] = "postgres"

G = nx.Graph()
connection = psycopg2.connect(**parameters)
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

cursor.execute("SELECT source, target, id FROM %s" % (table))
G.add_edges_from([(e[0],e[1],{"id":e[2]}) for e in cursor.fetchall()])

N = float(nx.number_of_edges(G))
connected_components = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
first_island = get_first_island(connected_components, N)
#print len(connected_components)
#print first_island

if first_island:
	isolated_edges = tuple([edge for island in connected_components[first_island:] for edge in nx.get_edge_attributes(island, "id").values()])
	cursor.execute("DELETE FROM " + table + " WHERE id IN %s", (isolated_edges,)) # Python gets mad if you remove that comma :-(

cursor.close()
connection.close()
