import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates


def plot_parallel_coordinates(parallel_coordinates_data: pd.DataFrame = None, title: str = "Parallel Coordinates Plot",
                              x_label: str = "Features", y_label: str = "Values"):
    """
    This function plots parallel coordinates for the given data. A parallel coordinates plot is a method for visualizing
    high-dimensional data, where each feature is represented as a vertical axis. Each data point is represented as a line,
    which connects the values of the features. This allows for the visualization of clusters and patterns in the data.

    Parameters
    ----------
    parallel_coordinates_data : pd.DataFrame
        The data to be visualized as parallel coordinates.
    title : str
        The title of the plot.
    x_label : str
        The label for the x-axis.
    y_label : str
        The label for the y-axis.

    Returns
    -------
    None

    """
    plt.figure(figsize=(18, 6))
    parallel_coordinates(parallel_coordinates_data, 'Cluster', colormap='viridis', linewidth=2, alpha=0.7)
    plt.xticks(rotation='vertical')
    plt.grid(visible=False)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Display the Legend
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


def plot_bar_chart(bar_chart_data: dict = None, title: str = "Bar Chart", x_label: str = "Features",
                   y_label: str = "Values"):
    """
    This function plots a bar chart for the given data. A bar chart is a method for visualizing categorical data, where the
    categories are represented as bars with heights proportional to the values they represent.

    Parameters
    ----------
    bar_chart_data : dict
        The data to be visualized as a bar chart.
    title : str
        The title of the plot.
    x_label : str
        The label for the x-axis.
    y_label : str
        The label for the y-axis.

    Returns
    -------
    None

    """
    plt.figure(figsize=(18, 6))
    plt.bar(bar_chart_data.keys(), bar_chart_data.values(), color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation='vertical')
    plt.show()


def plot_grouped_bar_chart(grouped_bar_chart_data: pd.DataFrame = None, title: str = "Grouped Bar Chart",
                           x_label: str = "Features", y_label: str = "Values"):
    """
    This function plots a grouped bar chart for the given data. A grouped bar chart is a method for visualizing categorical
    data, where the categories are represented as groups of bars with heights proportional to the values they represent.

    Parameters
    ----------
    grouped_bar_chart_data : pd.DataFrame
        The data to be visualized as a grouped bar chart.
    title : str
        The title of the plot.
    x_label : str
        The label for the x-axis.
    y_label : str
        The label for the y-axis.

    Returns
    -------
    None

    """
    grouped_bar_chart_data.plot(kind='bar', figsize=(18, 6),
                                color=['skyblue', 'salmon', 'lightgreen', 'orange', 'purple', 'cyan', 'yellow', 'pink',
                                       'red', 'blue'])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Show the Values on top of the bars, converting the values to string with 2 decimal places and , separator
    for p in plt.gca().patches:
        plt.gca().annotate(f'{p.get_height():,.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                           ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                           textcoords='offset points')
    plt.xticks(rotation='horizontal')
    plt.show()


def plot_line_chart(line_chart_data: pd.Series = None, title: str = "Line Chart", x_label: str = "Features",
                    y_label: str = "Values"):
    """
    This function plots a line chart for the given data. A line chart is a method for visualizing time-series data, where
    the values are represented as points connected by lines.

    Parameters
    ----------
    line_chart_data : pd.Series
        The data to be visualized as a line chart.
    title : str
        The title of the plot.
    x_label : str
        The label for the x-axis.
    y_label : str
        The label for the y-axis.

    Returns
    -------
    None

    """
    plt.figure(figsize=(18, 6))
    line_chart_data.plot(color='skyblue')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation='vertical')
    plt.grid(visible=False)
    plt.show()


def plot_moving_average(moving_average_data: pd.Series | pd.DataFrame = None, title: str = "Moving Average Plot",
                        x_label: str = "Features",
                        y_label: str = "Values", include_original_data_line: bool = False, window: int = 30):
    """
    This function plots a moving average plot for the given data. A moving average plot is a method for visualizing
    time-series data, where the values are represented as points connected by lines, and the moving average is also
    plotted to smooth out the data.

    Parameters
    ----------
    moving_average_data : pd.Series | pd.DataFrame
        The data to be visualized as a moving average plot.
    title : str
        The title of the plot.
    x_label : str
        The label for the x-axis.
    y_label : str
        The label for the y-axis.
    include_original_data_line : bool
        Whether to include the original data line in the plot.
    window : int
        The window size for the moving average.

    Returns
    -------
    None

    """
    plt.figure(figsize=(18, 6))
    if isinstance(moving_average_data, pd.Series):
        moving_average_data = moving_average_data.to_frame()
    if include_original_data_line:
        for column in moving_average_data.columns:
            moving_average_data[column].plot(linewidth=1, opacity=0.5, label=f"Original Data: {column}")
    for column in moving_average_data.columns:
        moving_average_data[column].rolling(window=window).mean().plot(linewidth=2,
                                                                       label=f"Moving Average: {column}")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation='vertical')
    plt.legend()
    plt.grid(visible=False)
    plt.show()
