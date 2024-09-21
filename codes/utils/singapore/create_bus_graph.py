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
def _graph_add_edge(graph, source, target, edge_attr):
    '''
    Add edge to graph
    Consider the parallel edges, the edge attributes are stored in list
    '''

    # Exist edge
    if graph.has_edge(source, target):
        for k, v in edge_attr.items():
            graph.edges[source, target][k].append(v)
    # Do not exist edge
    else:
        edge_attr = {k : [v] for k, v in edge_attr.items()}
        graph.add_edge(source, target, **edge_attr)

    return graph
# ==========================================================================================================
def graph_add_edges_l_sapce_from_dataframe(graph, data, node_id_col, edge_attr_list):
    '''
    add edges based row sequences of "data"
    L-space representation

    Relation between number of nodes and edges
    cycle = False : n_edge = n_node - 1
    cycle = True  : n_edge = n_node

    parameters:
    ---
    graph (networkx.Graph) :
    data (pandas.DataFrame) :
        data should be sorted by the order of nodes before calling this function
    node_id_col (str) :
    edge_attr_list (list) :
    cycle (bool, default=False) :
    '''
    assert graph.is_directed(), 'Only supported directed graph'

    # reset index, ensure the index is continuous from 0
    data = data.reset_index(drop=True)

    # number of edges (equals to start nodes)
    n_edge = data.shape[0] - 1

    # gradually add edges
    for ix in range(n_edge):
        node_start = data.loc[ix, node_id_col]
        node_end   = data.loc[ix+1, node_id_col]

        edge_attr = {col : data.loc[ix+1, col] for col in edge_attr_list}
        # add edge
        graph = _graph_add_edge(graph, node_start, node_end, edge_attr)

    # cycle line
    # if cycle:
    #     start_ix = data.shape[0] - 1
    #     end_ix   = 0
    #
    #     node_start = data.loc[start_ix, node_id_col]
    #     node_end   = data.loc[end_ix, node_id_col]
    #     edge_attr = {col : data.loc[start_ix, col] for col in edge_attr_list}
    #     # add edge
    #     graph = _graph_add_edge(graph, node_start, node_end, edge_attr)

    return graph
# ==========================================================================================================
def graph_add_edges_p_sapce_from_dataframe(graph, data, node_id_col, edge_attr_list):
    '''
    add edges based row sequences of "data"
    P-space representation
    no difference for whether the line is cycle or not

    Relation between number of nodes and edges
    cycle = False : n_edge = (n_node - 1) + (n_node - 2) + ... + 1
                           = n_node * (n_node - 1) / 2

    parameters:
    ---
    graph (networkx.Graph) :
    data (pandas.DataFrame) :
        data should be sorted by the order of nodes before calling this function
    node_id_col (str) :
    edge_attr_list (list) :
    cycle (bool, default=None) : Not affects for P-space representation
    '''

    assert not graph.is_directed(), 'Only supported undirected graph'

    # reset index, ensure the index is continuous from 0
    data = data.reset_index(drop=True)

    # number of start nodes
    n_edge = data.shape[0] - 1

    # gradually add edges
    for start in range(n_edge):
        for end in range(start + 1, n_edge + 1):
            node_start = data.loc[start, node_id_col]
            node_end = data.loc[end, node_id_col]
            edge_attr = {col : data.loc[end, col] for col in edge_attr_list}
            # add edge
            graph = _graph_add_edge(graph, node_start, node_end, edge_attr)

    # cycle line
    # P-space representation has same results for cycle and non-cycle lines

    return graph
# ==========================================================================================================
def create_graph_from_dataframe(
        data,
        node_id_col,
        order_col,
        mline_id_col,
        node_attr_list,
        edge_attr_list,
        space='l'):
    '''
    Parameters
    ---
    data (pandas.DataFrame) : metro station list
    node_id_col (str) : the column name of station unique id
        the "node_id_col" should be different for the transfer station (i.e., the station with same name) in different lines
    order_col (str) : the column name of station order
    mline_id_col (str) : the column name of metro line unique id
    # mline_cycle_col (str) : the column name indicating whether a metro line is cycle or not
    # all bus routes are assumed to be non-cycle
    node_attr_list (list) : the list of node attributes
    edge_attr_list (list) : the list of edge attributes
    space (str) : the space representation of metro network
        'l' or 'L' : L-space
        'p' or 'P' : P-space
    '''
    # check the data columns:
    _data_columns = data.columns.to_list()
    assert node_id_col in _data_columns, 'The "node_id_col" column should be in the data columns'
    assert order_col in _data_columns, 'The "order_col" column should be in the data columns'
    if isinstance(mline_id_col, str):
        assert mline_id_col in _data_columns, 'The "mline_id_col" column should be in the data columns'
    else:
        assert all([_col in _data_columns for _col in mline_id_col]), 'The "mline_id_col" column should be in the data columns'
    # assert mline_cycle_col in _data_columns, 'The "mline_cycle_col" column should be in the data columns'
    assert all([_col in _data_columns for _col in node_attr_list]), 'The node attribute columns should be in the data columns'
    assert all([_col in _data_columns for _col in edge_attr_list]), 'The edge attribute columns should be in the data columns'

    # check the node id
    # assert data[node_id_col].nunique() == data.shape[0], 'The node id should be unique'

    # undirected graph
    graph = nx.DiGraph()

    for line_name, line_station in tqdm.tqdm(data.groupby(mline_id_col), desc='Creating graph...'):

        # make sure the order is continuous
        line_station = line_station.astype({order_col : int}) \
            .sort_values(order_col) \
            .reset_index(drop=True)

        # number of station
        num_sta = line_station.shape[0]

        # is cycle line
        # is_cycle = line_station[mline_cycle_col].unique().tolist()
        # assert len(is_cycle) == 1, f'The circularity of bus line should be consistent, but got "{is_cycle}"'
        # is_cycle = is_cycle[0]

        # Step 1: add nodes
        # remove exits nodes
        node_li_in_graph = list(graph.nodes())
        node_li_add = set(line_station[node_id_col].tolist()).difference(set(node_li_in_graph))
        node_li_add = list(node_li_add)

        if len(node_li_add) > 0:
            node_list_df = line_station[line_station[node_id_col].isin(node_li_add)]
            graph = graph_add_nodes_from_dataframe(graph, node_list_df, node_id_col, node_attr_list)

        # Step 2: add edges
        if space in ['l', 'L']:
            graph = graph_add_edges_l_sapce_from_dataframe(graph, line_station, node_id_col, edge_attr_list)
        elif space in ['p', 'P']:
            graph = graph_add_edges_p_sapce_from_dataframe(graph, line_station, node_id_col, edge_attr_list)
        else:
            raise ValueError('The space should be either "L" or "P"')

    return graph
# ==========================================================================================================
#%%
