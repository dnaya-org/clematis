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

graph = Graph.Read(args.input)  # XXX should we support stdin?

assert(graph.is_dag())

system = System(graph, args.seed)

with sys.stdout if args.output == '-' else open(args.output, "w") as f:
    production = 0
    while production < 100:
        production = production + system.iterate(f)
