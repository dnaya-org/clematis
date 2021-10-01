import igraph

class System:

    def __init__(self, network):
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
        assert frozenset(network.vertex_attributes()) >= frozenset(['production_rate', 'failure_rate', 'id'])
        assert frozenset(network.edge_attributes()) >= frozenset(['buffer_size'])

        self.network_ = network
        self.time_ = 0

    def iterate(self, output):

        if self.time_ == 0:
            output.write("time,vertex,state\n")

        self.time_ = self.time_ + 1
