import tqdm
import pandas as pd
import networkx as nx


def graph_add_nodes_from_dataframe(graph, data, node_id_col, attr_list):
    '''
    '''
    for ix, row in data.iterrows():

        node_id = row[node_id_col]
        attr = {col : row[col] for col in attr_list}
        # add node
        graph.add_node(node_id, **attr)

    return graph
# ==========================================================================================================
def graph_add_edges_l_sapce_from_dataframe(graph, data, node_id_col, attr_list, cycle=False):
    '''
    add edges based row sequences of "data"
    L-space representation

    Relation between number of nodes and edges
    cycle = False : n_edge = n_node - 1
    cycle = True  : n_edge = n_node
    '''
    # reset index, ensure the index is continuous from 0
    data = data.reset_index(drop=True)

    # number of edges (equals to start nodes)
    n_edge = data.shape[0] - 1

    # gradually add edges
    for ix in range(n_edge):
        node_start = data.loc[ix, node_id_col]
        node_end   = data.loc[ix+1, node_id_col]
        attr = {col : data.loc[ix, col] for col in attr_list}
        # add edge
        graph.add_edge(node_start, node_end, **attr)

    # cycle line
    if cycle:

        start_ix = data.shape[0] - 1
        end_ix   = 0

        node_start = data.loc[start_ix, node_id_col]
        node_end   = data.loc[end_ix, node_id_col]
        attr = {col : data.loc[start_ix, col] for col in attr_list}
        # add edge
        graph.add_edge(node_start, node_end, **attr)

    return graph
# ==========================================================================================================
def graph_add_edges_p_sapce_from_dataframe(graph, data, node_id_col, attr_list, cycle=None):
    '''
    add edges based row sequences of "data"
    P-space representation
    no difference for whether the line is cycle or not

    Relation between number of nodes and edges
    cycle = False : n_edge = (n_node - 1) + (n_node - 2) + ... + 1
                           = n_node * (n_node - 1) / 2

    '''
    # reset index, ensure the index is continuous from 0
    data = data.reset_index(drop=True)

    # number of start nodes
    n_edge = data.shape[0] - 1

    # gradually add edges
    for start in range(n_edge):
        for end in range(start + 1, n_edge + 1):

            node_start = data.loc[start, node_id_col]
            node_end = data.loc[end, node_id_col]
            attr = {col : data.loc[start, col] for col in attr_list}
            # add edge
            graph.add_edge(node_start, node_end, **attr)

    # cycle line
    # there is no difference for cycle line

    return graph
# ==========================================================================================================
def create_graph_from_dataframe(data, node_id_col, order_col, line_name_col, flag_cycle_col, node_attr_list, edge_attr_list, space='l'):
    '''

    '''
    # check the node id
    assert data[node_id_col].nunique() == data.shape[0], 'The node id should be unique'

    # undirected graph
    graph = nx.Graph()

    for line_name, line_station in tqdm.tqdm(data.groupby(line_name_col), desc='Creating graph'):

        #
        line_station = line_station.astype({order_col : int}) \
            .sort_values(order_col) \
            .reset_index(drop=True)

        # number of station
        num_sta = line_station.shape[0]

        # is cycle line
        is_cycle = line_station[flag_cycle_col].unique().tolist()
        assert len(is_cycle) == 1, f'The circularity of metro line should be consistent, but got "{is_cycle}"'
        is_cycle = is_cycle[0]

        # add nodes
        graph = graph_add_nodes_from_dataframe(graph, line_station, node_id_col, node_attr_list)

        # add edges
        if space in ['l', 'L']:
            graph = graph_add_edges_l_sapce_from_dataframe(graph, line_station, node_id_col, edge_attr_list, cycle=is_cycle)
        elif space in ['p', 'P']:
            graph = graph_add_edges_p_sapce_from_dataframe(graph, line_station, node_id_col, edge_attr_list, cycle=None)
        else:
            raise ValueError('The space should be either l or p')

    return graph
# ==========================================================================================================
