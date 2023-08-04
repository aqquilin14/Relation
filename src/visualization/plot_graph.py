from constants import OUTPUT_PATH, OUTPUT_FORMAT
from graph import Graph
import matplotlib.pyplot as plt
import networkx as nx


class GraphPlot:

    def __init__(self, graph: Graph, figure_size: tuple[int, int] = (15, 15), node_size: int = 500, font_size: int = 10,
                 spring_iter: int = 25, spring_k: int = 0.75):
        self.graph: Graph = graph

        self.figure_size = figure_size
        self.node_size = node_size
        self.font_size = font_size
        self.spring_iter = spring_iter
        self.spring_k = spring_k

        self.xgraph: nx.Graph = self.get_nxgraph()

    def get_nxgraph(self) -> nx.Graph:
        xgraph = nx.DiGraph()

        for node in self.graph.nodes:
            xgraph.add_node(node.get_uri())

        for antecedent, edge_label, consequent in self.graph.edges:
            xgraph.add_edge(antecedent.get_uri(), consequent.get_uri())

        return xgraph

    def plot_graph(self) -> None:
        fig = plt.figure(figsize=self.figure_size)
        pos = nx.spring_layout(self.xgraph, k=self.spring_k, iterations=self.spring_iter)
        nx.draw(self.xgraph, with_labels=True, node_size=self.node_size, font_size=self.font_size, pos=pos)
        plt.savefig(OUTPUT_PATH, format=OUTPUT_FORMAT)
