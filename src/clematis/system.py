import igraph
import numpy as np


class System:

    def __init__(self, network, seed):
        """
        Parameters
        ----------
        network: igraph.Graph
            Manufacturing system topological and dynamical properties.
            Must be a DAG with the vertex properties `production_rate` and
            `failure_rate` (between 0 and 1).  Edges must have an integer
            property called `buffer_size` greater than 0.
        """
        assert network.is_dag()
        assert frozenset(network.vertex_attributes()) >= frozenset(
            ['production_rate', 'failure_rate', 'id'])
        assert frozenset(
            network.edge_attributes()) >= frozenset(
            ['buffer_size'])

        self._network = network
        self._time = 0

        self._buffer = np.array([0.0 for i in range(network.ecount())])
        self._state = np.array(['starved' for i in range(network.vcount())])

        self._rng = np.random.default_rng(seed=seed)

    def iterate(self, output):

        total_production = 0

        if self._time == 0:
            output.write("time,vertex,state\n")

        self._time = self._time + 1

        ids = self._network.vs['id']
        prate = np.array(self._network.vs['production_rate'])
        frate = np.array(self._network.vs['failure_rate'])
        buffer_size = np.array(self._network.es['buffer_size'])

        for i in self._network.topological_sorting():
            in_edges = [edge.index for edge in self._network.vs[i].in_edges()]
            out_edges = [
                edge.index for edge in self._network.vs[i].out_edges()]

            if len(out_edges) > 0 and np.all(
                    self._buffer[out_edges] >= buffer_size[out_edges]):
                self._state[i] = 'blocked'
            elif len(in_edges) == 0:
                self._state[i] = 'working'
            elif np.any(self._buffer[in_edges] == 0):
                self._state[i] = 'starved'
            else:
                self._state[i] = 'working'

            if self._state[i] == 'working':

                if self._rng.random() < frate[i]:
                    continue

                production = prate[i]
                if len(in_edges) > 0:
                    production = min(
                        production, np.min(
                            self._buffer[in_edges]))
                if len(out_edges) > 0:
                    eligible = np.array(out_edges)[
                        self._buffer[out_edges] < buffer_size[out_edges]]
                    assert len(eligible) > 0
                    to = self._rng.choice(eligible, 1)[0]
                    production = min(
                        production, buffer_size[to] - self._buffer[to])

                if len(in_edges) > 0:
                    self._buffer[in_edges] = self._buffer[in_edges] - production

                if len(out_edges) > 0:
                    self._buffer[to] = self._buffer[to] + production
                else:
                    total_production = total_production + production

            output.write(
                "{},{},{}\n".format(
                    self._time,
                    ids[i],
                    self._state[i]))

        return total_production
