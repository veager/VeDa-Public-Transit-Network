import re
import matplotlib.pyplot as plt



#%%
def _sorted_labels(handles, labels):

    assert len(labels) == len(handles), 'Length of labels and handles should be the same.'

    # label with number
    label_num = []
    index_num = []

    # label with alphabet only
    label_alp = []
    index_alp = []

    for ix, l in enumerate(labels):
        if re.search(r'\d+', l) is None:
            label_alp.append(l)
            index_alp.append(ix)
        else:
            label_num.append(l)
            index_num.append(ix)

    index_alp, _ = zip(*sorted(zip(index_alp, label_alp), key=lambda x : x[1]))
    index_num, _ = zip(*sorted(zip(index_num, label_num), key = lambda x : int(re.search(r'\d+', x[1]).group(0))))
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
    print(labels)

    return ax
# ==============================================================================================
#%%
