import sys

from . import System
from igraph import Graph

assert len(sys.argv) == 2
graph = Graph.Read(sys.argv[1])

print(graph)
assert(graph.is_dag())

print(graph.vs["production_rate"])
print(graph.vs["failure_rate"])
print(graph.es["buffer_size"])
