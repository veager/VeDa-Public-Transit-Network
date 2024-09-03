import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


def print_graph_basic_information(graph):

    print(
        '\nDirected:', graph.is_directed(),
        '\nNumber of nodes:', graph.number_of_nodes(),
        '\nNumber of edges:', graph.number_of_edges(),
        # '\nNode ids:', graph.nodes(),
        # '\nEdge ids:', graph.edges()
    )
# ==========================================================================================================
def plot_geographical_graph(graph, x, y, color):

    nodes = pd.DataFrame((graph.nodes(data=True)))


    fig, ax = plt.subplots()

