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
