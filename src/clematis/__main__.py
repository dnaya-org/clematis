import argparse
import sys

from . import System
from igraph import Graph

parser = argparse.ArgumentParser(
    description='Complex Manufacturing Simulation')

parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--seed', type=int, required=True)

args = parser.parse_args()
print(args)

graph = Graph.Read(args.input) # XXX should we support stdin?

print(graph)
assert(graph.is_dag())

print(graph.vs["production_rate"])
print(graph.vs["failure_rate"])
print(graph.es["buffer_size"])

system = System(graph)

if args.output == '-':
    system.iterate(sys.stdout)
else:
    with open(args.output, "w") as f:
        system.iterate(f)
