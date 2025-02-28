from typing import List, Union, Dict, Any
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pathlib import Path

def create_figure(figsize: tuple[float, float] = (3, 1.6)) -> Figure:
    """Create and initialize a matplotlib figure"""
    return plt.figure(figsize=figsize)

def prepare_data(identifier: Union[Dict[Any, float], List[float]]) -> tuple[List[int], List[float]]:
    """Convert input data to plottable format"""
    values = list(identifier.values()) if isinstance(identifier, dict) else identifier
    x_values = list(range(1, len(values) + 1))
    return x_values, values

def should_plot(data: List[float], threshold: float = 0.003) -> bool:
    """Determine if data should be plotted based on threshold"""
    return len(data) < 1 or max(data) < threshold

def set_plot_attributes(
    title: str = '',
    xlabel: str = '',
    ylabel: str = '',
    fontsize: int = 7,
    title_size: int = 10
) -> None:
    """Set plot attributes with consistent styling"""
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.title(title, fontsize=title_size)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

def save_and_show_plot(
    save_path: Union[str, Path],
    format: str = 'pdf',
    bbox_inches: str = 'tight',
    pad_inches: float = 0.01
) -> None:
    """Save plot to file and display"""
    plt.savefig(save_path, format=format, bbox_inches=bbox_inches, pad_inches=pad_inches)
    plt.show()
    
    current_figsize = plt.gcf().get_size_inches()

def draw(
    identifiers: List[Union[Dict[Any, float], List[float]]],
    title: str = '',
    xlabel: str = '',
    ylabel: str = '',
    save_path: Union[str, Path] = './figure.pdf'
) -> None:
    """
    Draw multiple data series in a single plot with consistent styling
    
    Args:
        identifiers: List of data series to plot
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        save_path: Path to save the output PDF
    """
    create_figure()
    
    # Plot data
    plot_config = {
        'linewidth': 0.5,
        'color': 'red',
        'alpha': 0.01
    }
    
    for identifier in identifiers:
        x_values, values = prepare_data(identifier)
        if should_plot(values):
            plt.plot(x_values, values, **plot_config)
    
    # Set attributes and save
    set_plot_attributes(title, xlabel, ylabel)
    save_and_show_plot(save_path)

# Create partially applied functions for common use cases
draw_with_default_path = partial(draw, save_path='./output/figure.pdf')
draw_time_series = partial(
    draw,
    xlabel='Sequence Number',
    ylabel='Value'
)