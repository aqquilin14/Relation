from constants import INPUT_PATH
from extract_graph import ExtractGraph
from plot_graph import GraphPlot


if __name__ == '__main__':
    graph = ExtractGraph(INPUT_PATH).get_graph()
    GraphPlot(graph).plot_graph()

