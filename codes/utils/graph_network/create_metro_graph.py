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

    parameters:
    ---
    graph (networkx.Graph) :
    data (pandas.DataFrame) :
        data should be sorted by the order of nodes before calling this function
    node_id_col (str) :
    attr_list (list) :
    cycle (bool, default=False) :
    '''
    assert not graph.is_directed(), 'Only supported undirected graph'

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

    parameters:
    ---
    graph (networkx.Graph) :
    data (pandas.DataFrame) :
        data should be sorted by the order of nodes before calling this function
    node_id_col (str) :
    attr_list (list) :
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
            attr = {col : data.loc[start, col] for col in attr_list}
            # add edge
            graph.add_edge(node_start, node_end, **attr)

    # cycle line
    # P-space representation has same results for cycle and non-cycle lines

    return graph
# ==========================================================================================================
def create_graph_from_dataframe(
    data,
    node_id_col,
    order_col,
    mline_id_col,
    mline_cycle_col,
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
    mline_cycle_col (str) : the column name indicating whether a metro line is cycle or not
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
    assert mline_id_col in _data_columns, 'The "mline_id_col" column should be in the data columns'
    assert mline_cycle_col in _data_columns, 'The "mline_cycle_col" column should be in the data columns'
    assert all([_col in _data_columns for _col in node_attr_list]), 'The node attribute columns should be in the data columns'
    assert all([_col in _data_columns for _col in edge_attr_list]), 'The edge attribute columns should be in the data columns'

    # check the node id
    assert data[node_id_col].nunique() == data.shape[0], 'The node id should be unique'

    # undirected graph
    graph = nx.Graph()

    for line_name, line_station in tqdm.tqdm(data.groupby(mline_id_col), desc='Creating graph...'):

        # make sure the order is continuous
        line_station = line_station.astype({order_col : int}) \
            .sort_values(order_col) \
            .reset_index(drop=True)

        # number of station
        num_sta = line_station.shape[0]

        # is cycle line
        is_cycle = line_station[mline_cycle_col].unique().tolist()
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
            raise ValueError('The space should be either "L" or "P"')

    return graph
# ==========================================================================================================
def graph_add_transfer_edges_from_dataframe(
    graph,
    data,
    node_id_col,
    transfer_name_col,
    attr_list_unique,
    attr_list_merged = None,
    merge_transfer_node = False
):
    '''
    add transfer edges of metro network, the station with same name will be deemed as the same station

    Parameters
    ----------
    graph : networkx.Graph
        the graph object
    data : pandas.DataFrame
        transfer station list
    node_id_col : str
        the column name of node unique id
    transfer_name_col : str
        the column name indicating transfer station, the station with same name ("transfer_name_col") will be deemed as the transfer station
    attr_list_unique : list
        column list used from unique attribute of merged nodes
    attr_list_merged : list
        column list used from merged attribute of merged nodes
    merge_transfer_node : bool
        whether to merge transfer stations into one node
        merge_transfer_node = False: add virtual transfer edges between transfer stations
    '''
    assert not graph.is_directed(), 'Only supported undirected graph'
    if not merge_transfer_node:
        assert attr_list_merged is None, 'The "attr_list_merged" should be None when set "merge_transfer_node=False", as node attributes of transfer station are no needed to merged'

    for stn_name, stn_data in data.groupby(transfer_name_col):

        stn_data = stn_data.reset_index(drop=True)
        num_stn = stn_data.shape[0]

        # assert stn_data['line_name'].nunique() > 1, 'The transfer station should be in at least two different lines'
        assert num_stn >= 2, f'The number of transfer line should be greater or equal to 2, but got {num_stn}'

        # merge the transfer stations in different lines
        if merge_transfer_node:
            # node attributes
            # -- location
            attr_dict = {'transfer' : True}
            for _attr_col in attr_list_unique:
                attr_dict[_attr_col] = stn_data.loc[0, _attr_col]
            # -- other attributes
            for _attr_col in attr_list_merged:
                attr_dict[_attr_col] = ','.join(list(set(stn_data[_attr_col].to_list())))

            # add a virtual node
            graph.add_node('t', **attr_dict)

            node_list = stn_data[node_id_col].tolist()

            # add edges
            for node in node_list:
                # add edge between the node's neighbors and the virtual node
                for neigh in graph.neighbors(node):
                    graph.add_edge('t', neigh, **graph.get_edge_data(node, neigh))
                # remove the node
                graph.remove_node(node)

            # relabel the virtual node
            graph = nx.relabel_nodes(graph, mapping={'t' : node_list[0]})

        # add virtual transfer edges
        else:
            if num_stn == 2:
                node_start = stn_data.loc[0, node_id_col]
                node_end   = stn_data.loc[1, node_id_col]
                graph.add_edge(node_start, node_end, transfer_edge=True)

            else:
                for i in range(num_stn - 1):
                    for j in range(i + 1, num_stn):
                        node_start = stn_data.loc[i, node_id_col]
                        node_end   = stn_data.loc[j, node_id_col]
                        graph.add_edge(node_start, node_end, transfer_edge=True)

    return graph
# ==============================================================================================
