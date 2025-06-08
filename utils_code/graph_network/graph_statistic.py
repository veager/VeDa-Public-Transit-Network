import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


def _get_giant_component(graph):

    if nx.is_directed(graph):
        giant_com = sorted(nx.weakly_connected_components(graph), key=len, reverse=True)
    elif not nx.is_directed(graph):
        giant_com = sorted(nx.connected_components(graph), key=len, reverse=True)

    giant_com = graph.subgraph(giant_com[0])

    return graph
# ============================================================================================
def print_graph_basic_information(graph):

    print('\nIs directed: ', nx.is_directed(graph),
          '\nNumber of nodes: ', graph.number_of_nodes(),
          '\nNumber of edges: ', graph.number_of_edges(),
          '\nNumber of isolated nodes: ', len(list(nx.isolates(graph))),
          '\nNumber of self-loops: ', nx.number_of_selfloops(graph))

    # Get the giant component
    giant_com = _get_giant_component(graph)
    print('\nThe giant component: ',
          '\nNumber of nodes: ', giant_com.number_of_nodes(),
          '\nNumber of edges: ', giant_com.number_of_edges())

    if not nx.is_directed(graph):
        print('Number of connected components: ', nx.number_connected_components(graph))
    elif nx.is_directed(graph):
        print('Number of (weekly) connected components: ', nx.number_weakly_connected_components(graph))
# ============================================================================================
