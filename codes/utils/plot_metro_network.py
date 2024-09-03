import re
import matplotlib.pyplot as plt



#%%
def _sorted_labels(handles, labels):

    assert len(labels) == len(handles), 'Length of labels and handles should be the same.'

    # label with alphabet only
    label_alp = []
    index_alp = []

    # label with number
    label_num = []
    index_num = []

    for ix, l in enumerate(labels):
        if re.search(r'\d+', l) is None:
            label_alp.append(l)
            index_alp.append(ix)
        else:
            label_num.append(l)
            index_num.append(ix)

    # print(index_alp, index_num)

    if len(index_alp) > 0:
        index_alp, _ = zip(*sorted(zip(index_alp, label_alp), key=lambda x : x[1]))
        index_alp = list(index_alp)

    if len(index_num) > 0:
        index_num, _ = zip(*sorted(zip(index_num, label_num), key = lambda x : int(re.search(r'\d+', x[1]).group(0))))
        index_num = list(index_num)

    # sorted index
    index_sorted = index_num + index_alp

    # sorted labels
    labels_sorted = [labels[ix] for ix in index_sorted]
    # sorted values
    handles_sorted = [handles[ix] for ix in index_sorted]

    return handles_sorted, labels_sorted
# ======================================================================================================================



def plot_metro_network_separate_from_dataframe(
    data,
    x_col, y_col,
    n_col = 3, subplot_size = (4, 3), shared_axis = False,
    plot_background = False,
    line_kwargs = None,
):
    # line arguments, do not add "color"
    line_kwargs_default = dict(marker='o', markersize=5)
    if line_kwargs is not None:
        line_kwargs_default.update(line_kwargs)

    # number of subplots
    n_subplot = data['line_name'].nunique()
    n_row = n_subplot // n_col + 1

    # figure initialization
    fig, axes = plt.subplots(
        n_row, n_col,
        figsize = (n_col * subplot_size[0], n_row * subplot_size[1]),
        sharex = shared_axis, sharey = shared_axis)
    axes = axes.flatten()

    #
    for ix, (line_name, data_line) in enumerate(data.groupby('line_name')):

        ax = axes[ix]
        ax.set_title(line_name)

        # using the whole network as background
        if plot_background:
            ax = plot_metro_network_integrate_from_dataframe(
                data, x_col, y_col, ax = ax,
                line_kwargs=dict(alpha=0.5, color='grey', markersize=2))

        # line color
        line_color = data_line['line_color'].unique().tolist()[0]
        # line
        handle = ax.plot(
            data_line[x_col].values, data_line[y_col].values, c=line_color,
            label=line_name,
            **line_kwargs_default)

        ax.legend([handle[0]], [line_name])

        # text
        for i, row in data_line.iterrows():
            ax.text(row[x_col], row[y_col], row['no'], fontsize=8)

    plt.tight_layout(w_pad=0, h_pad=0.)
# ==============================================================================================


def plot_metro_network_integrate_from_dataframe(
    data,
    x_col, y_col,
    ax = None,
    line_kwargs = None,
):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize = (12, 12))

    # line arguments
    line_kwargs_default = dict(marker='.', markersize=1.5, lw=2)
    if line_kwargs is not None:
        line_kwargs_default.update(line_kwargs)

    # plot
    for ix, (line_name, data_line) in enumerate(data.groupby('line_name')):

        # line color
        line_color = data_line['line_color'].unique().tolist()[0]

        # plot line
        if 'color' not in line_kwargs_default:
            ax.plot(data_line[x_col].values, data_line[y_col].values,
                    color = line_color,
                    label = line_name,
                    **line_kwargs_default)
        else:
            ax.plot(data_line[x_col].values, data_line[y_col].values,
                    label = line_name,
                    **line_kwargs_default)

    # add legend
    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    handles, labels = _sorted_labels(handles, labels)
    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    return ax
# ==============================================================================================

def plot_geographical_graph_edge(graph, x_col, y_col, label_col, color_col, ax=None):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.set_aspect('equal', 'box')

    # plot edges
    legend_handles = []
    legend_labels = []

    for (node_start, node_end, edge_attr) in graph.edges(data=True):

        x1, y1 = graph.nodes(data=True)[node_start][x_col], graph.nodes(data=True)[node_start][y_col]
        x2, y2 = graph.nodes(data=True)[node_end][x_col], graph.nodes(data=True)[node_end][y_col]

        try:
            color = edge_attr[color_col]
        except:
            color = 'grey'

        try:
            label = edge_attr[label_col]
        except:
            label = None

        handle = ax.plot(
            [x1, x2], [y1, y2], c=color,
            lw=1.5, alpha=1, label=label)

        if label not in legend_labels:
            legend_handles.append(handle[0])
            legend_labels.append(label)

    handles, labels = _sorted_labels(legend_handles, legend_labels)

    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    return ax
# ==============================================================================================
