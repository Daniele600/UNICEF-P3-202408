import matplotlib.pyplot as plt


def _add_text_to_bar(bars, axis):
    for bar in bars:
        height = bar.get_height()
        txt = f"{round(height,1)}%"
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            txt,
            ha="center",
            va="bottom",
        )


def _create_barchart(labels, values, title, color, ax):
    bars = ax.bar(labels, values, color=color)
    ax.set_title(title)
    ax.set_ylim(0, 100)
    ax.grid("on", axis="y")
    return bars


def plot_bars(
    values1: list,
    values2: list,
    labels1: list,
    labels2: list,
    chart_title1: str,
    chart_title2: str,
):
    """
    Plots two barchart, each barchart has two values.

    Args:
        values1: A two elements list containing floats (first chart)
        values2: A two elements list containing floats (second chart)
        labels1: A two elements list containing the labels for the first 2 values
        labels2: A two elements list containing the labels for the second 2 values
        chart_title1: The title for the first chart
        chart_title2: The title for the second chart
    """

    # Creating a figure and axis objects
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    # Bar chart 1
    bars1 = _create_barchart(labels1, values1, chart_title1, "blue", ax1)

    # Bar chart 2
    bars2 = _create_barchart(labels2, values2, chart_title2, "green", ax2)
    # Show the values on the chart
    _add_text_to_bar(bars1, ax1)
    _add_text_to_bar(bars2, ax2)

    text = " Put some text here"

    # # Adjust layout to make space for the text box
    ax3.axis("off")
    ax3.text(0, 1, text)

    # Display the plots
    plt.tight_layout()
    plt.show()
