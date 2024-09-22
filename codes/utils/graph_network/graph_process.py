import tqdm
import networkx as nx

# ============================================================================================
def save_graph_to_file(graph, path, graph_name, fmt=['gexf', 'gml', 'graphml'], backup=False):

    # save path
    save_path = path + '/' + graph_name

    # file format
    supported_fmt = ['gexf', 'graphml', 'edgelist']

    if isinstance(fmt, str):
        fmt = [fmt]
    elif not isinstance(fmt, list):
        raise ValueError('fmt must be a list or a string')

    assert any([f not in supported_fmt for f in fmt]), 'file format "fmt" only support "gexf", "graphml", or "edgelist"'


    for f in tqdm.tqdm(fmt, desc='Saving graph'):
        if f == 'gexf':
            file_path = save_path + '.gexf'
            nx.write_gexf(graph, file_path)

            if backup:
                nx.write_gexf(graph, file_path + '.backup')

        elif f == 'gml':
            file_path = save_path + '.gml'
            nx.write_gml(graph, file_path)

            if backup:
                nx.write_gml(graph, file_path + '.backup')

        elif f == 'graphml':
            file_path = save_path + '.graphml'
            nx.write_graphml(graph, file_path)

            if backup:
                nx.write_graphml(graph, file_path + '.backup')
# ============================================================================================
#%%
