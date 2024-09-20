import re
import matplotlib.pyplot as plt


#%%
def _sorted_labels_numeric(handles, labels):

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
def _sorted_labels(handles, labels, sort_type):

    assert len(labels) == len(handles), 'Length of labels and handles should be the same.'

    if sort_type is None:
        pass

    elif isinstance(sort_type, list):
        # sorted by a given order
        assert len(sort_type) == len(labels), 'The Lengths of "sort_type" and "labels" must be same.'
        assert set(sort_type) == set(labels), 'The elements of "sort_type" and "labels" must be same.'

        # a sorted order dict, values indicate the index
        _sorted_order = {l : ix for ix, l in enumerate(sort_type)}
        handles, labels = zip(*sorted(zip(handles, labels), key=lambda x : _sorted_order[x[1]]))

    elif isinstance(sort_type, str):
        # sorted by numeric
        # used for the case like [line1, line2, line3, ...]
        if sort_type in ['numeric']:
            handles, labels = _sorted_labels_numeric(handles, labels)

        elif sort_type in ['alphabet']:
            handles, labels = zip(*sorted(zip(handles, labels), key=lambda x : x[1]))
        else:
            raise ValueError('The sort type should be either "numeric" or "alphabet"')
    else:
        raise ValueError('The sort type should be either list or str')

    return handles, labels
# ======================================================================================================================

def plot_metro_network_separate_from_dataframe(
    data,
    x_col, y_col,
    mline_id_col, mline_label_col, mline_color_col, mline_cycle_col,
    node_label_col,
    n_col = 3, subplot_size = (4, 3), shared_axis = False,
    plot_background = False,
    line_kwargs = None,
):
    # line arguments, do not add "color"
    line_kwargs_default = dict(marker='o', markersize=5)
    if line_kwargs is not None:
        line_kwargs_default.update(line_kwargs)

    # number of subplots
    n_subplot = data[mline_id_col].nunique()
    n_row = n_subplot // n_col + 1

    # figure initialization
    fig, axes = plt.subplots(
        n_row, n_col,
        figsize = (n_col * subplot_size[0], n_row * subplot_size[1]),
        sharex = shared_axis, sharey = shared_axis)
    axes = axes.flatten()

    #
    for ix, (mline_id, data_line) in enumerate(data.groupby(mline_id_col)):

        # line color
        mline_color = data_line[mline_color_col].unique().tolist()[0]
        # line label
        mline_label = data_line[mline_label_col].unique().tolist()[0]
        # line cycle
        mline_cycle = data_line[mline_cycle_col].unique().tolist()[0]

        ax = axes[ix]
        ax.set_title(mline_label)

        # using the whole network as background
        if plot_background:
            ax = plot_metro_network_integrate_from_dataframe(
                data, x_col, y_col,
                ax = ax,
                mline_id_col = mline_id_col,
                mline_label_col = mline_label_col,
                mline_color_col = mline_color_col,
                mline_cycle_col = mline_cycle_col,
                line_kwargs = dict(alpha=0.5, color='grey', markersize=2))

        # line data
        plot_d_x = data_line[x_col].values.tolist()
        plot_d_y = data_line[y_col].values.tolist()
        if mline_cycle:
            plot_d_x.append(plot_d_x[0])
            plot_d_y.append(plot_d_y[0])

        # line
        handle = ax.plot(
            plot_d_x, plot_d_y,
            c=mline_color,
            label=mline_label,
            **line_kwargs_default)

        ax.legend([handle[0]], [mline_label])

        # text
        for i, row in data_line.iterrows():
            ax.text(row[x_col], row[y_col], row[node_label_col], fontsize=8)

    plt.tight_layout(w_pad=0, h_pad=0.)
# ==============================================================================================


def plot_metro_network_integrate_from_dataframe(
    data,
    x_col, y_col,
    mline_id_col, mline_label_col, mline_color_col, mline_cycle_col,
    sort_legend = True,
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
    for ix, (mline_id, data_line) in enumerate(data.groupby(mline_id_col)):

        # line color
        mline_color = data_line[mline_color_col].unique().tolist()[0]
        # line label
        mline_label = data_line[mline_label_col].unique().tolist()[0]
        # line cycle
        mline_cycle = data_line[mline_cycle_col].unique().tolist()[0]

        # data
        _plot_d_x = data_line[x_col].values.tolist()
        _plot_d_y = data_line[y_col].values.tolist()
        if mline_cycle:
            _plot_d_x.append(_plot_d_x[0])
            _plot_d_y.append(_plot_d_y[0])

        # plot line
        if 'color' not in line_kwargs_default:
            ax.plot(_plot_d_x, _plot_d_y,
                    color = mline_color,
                    label = mline_label,
                    **line_kwargs_default)
        else:
            ax.plot(_plot_d_x,_plot_d_y,
                    label = mline_label,
                    **line_kwargs_default)

    # add legend
    ax.legend()
    handles, labels = ax.get_legend_handles_labels()
    handles, labels = _sorted_labels(handles, labels, sort_type=sort_legend)
    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    return ax
# ==============================================================================================

def plot_geographical_graph_edge(
    graph,
    x_col, y_col,
    mline_label, mline_color,
    sort_legend = 'numeric',
    ax = None
):

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
            color = edge_attr[mline_color]
        except:
            color = 'grey'

        try:
            label = edge_attr[mline_label]
        except:
            label = None

        handle = ax.plot(
            [x1, x2], [y1, y2], c=color,
            lw=1.5, alpha=1, label=label)

        if label not in legend_labels:
            legend_handles.append(handle[0])
            legend_labels.append(label)

    handles, labels = _sorted_labels(legend_handles, legend_labels, sort_type=sort_legend)

    ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    return ax
# ==============================================================================================
