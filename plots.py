from matplotlib import colors as clrs
from matplotlib import pyplot as plt
from PIL import Image
from PIL import PyAccess

# neumora color palette
orange = '#F88337'
green = '#5AD976'
purple = '#CCCCFF'
blue = '#66CCFF'


SEABORN_PALETTES = dict(
    husl8=['#f77189', '#ce9032', '#97a431', '#32b166', '#36ada4', '#39a7d0',
           '#a48cf4', '#f561dd'],
    deep=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"],
    deep6=["#4C72B0", "#55A868", "#C44E52",
           "#8172B3", "#CCB974", "#64B5CD"],
    muted=["#4878D0", "#EE854A", "#6ACC64", "#D65F5F", "#956CB4",
           "#8C613C", "#DC7EC0", "#797979", "#D5BB67", "#82C6E2"],
    muted6=["#4878D0", "#6ACC64", "#D65F5F",
            "#956CB4", "#D5BB67", "#82C6E2"],
    pastel=["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"],
    pastel6=["#A1C9F4", "#8DE5A1", "#FF9F9B",
             "#D0BBFF", "#FFFEA3", "#B9F2F0"],
    bright=["#023EFF", "#FF7C00", "#1AC938", "#E8000B", "#8B2BE2",
            "#9F4800", "#F14CC1", "#A3A3A3", "#FFC400", "#00D7FF"],
    bright6=["#023EFF", "#1AC938", "#E8000B",
             "#8B2BE2", "#FFC400", "#00D7FF"],
    dark=["#001C7F", "#B1400D", "#12711C", "#8C0800", "#591E71",
          "#592F0D", "#A23582", "#3C3C3C", "#B8850A", "#006374"],
    dark6=["#001C7F", "#12711C", "#8C0800",
           "#591E71", "#B8850A", "#006374"],
    colorblind=["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
                "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9"],
    colorblind6=["#0173B2", "#029E73", "#D55E00",
                 "#CC78BC", "#ECE133", "#56B4E9"]
)



def unique_color_cmap(n, cmap='hsv'):
    """
    Return a function that maps each index in 0, ... n-1 to a unique color.

    Parameters
    ----------
    n : int
        number of unique colors
    cmap : str
        colormap name

    Returns
    -------
    callable
        matplotlib.colors.ScalarMappable object

    """
    import matplotlib.cm as cmx
    import matplotlib.colors as colors

    color_norm = colors.Normalize(vmin=0, vmax=n - 1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=cmap)

    def map_index_to_rgb_color(index):
        """Generate cmx.ScalarMappable from integer index to unique color. """
        return scalar_map.to_rgba(index)

    return map_index_to_rgb_color



def adjust_luminosity(color, amount=0.75):
    """
    Adjust luminosity of a color.

    Source: https://stackoverflow.com/a/49601444/6447032

    Parameters
    ----------
    color : str or tuple
        hex string, matplotlib color string, or rgb tuple
    amount : float
        amount of adjustment; values above (below) 1 lighten (darken) color

    Returns
    -------
    str
        adjusted color as a hex string

    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    # noinspection PyTypeChecker
    tmp = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return mc.rgb2hex(tmp)


def rgb2hex(rgb: list, keep_alpha=False) -> str:
    return clrs.to_hex(rgb, keep_alpha=keep_alpha)


def hex2rgb(color: str):
    return clrs.to_rgb(color)


def remove_spines(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# noinspection PyTypeChecker
def detach(ax, which='both', xpad=0.05, ypad=0.05):
    """
    Create separation between data and axis spines/ticks.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        axes instance
    which : str
        which axis to detach {'y', 'x'}
    xpad : float
        fraction of x-axis size with which to pad
    ypad : float
        fraction of y-axis size with which to pad

    """
    if which == 'y':
        current_ticks = ax.yaxis.get_ticklocs()
        ax.set_ylim(
            (current_ticks[0] - current_ticks[-1] * ypad,
             current_ticks[-1] * (1.0 + ypad)))
        ax.set_yticks(current_ticks)
        ax.spines['left'].set_bounds(current_ticks[0], current_ticks[-1])
    elif which == 'x':
        current_ticks = ax.xaxis.get_ticklocs()
        ax.set_xlim(
            (current_ticks[0] - current_ticks[-1] * xpad,
             current_ticks[-1] * (1.0 + xpad)))
        ax.set_xticks(current_ticks)
        ax.spines['bottom'].set_bounds(current_ticks[0], current_ticks[-1])
    elif which == 'both':
        current_xticks = ax.xaxis.get_ticklocs()
        xtick_range = current_xticks[-1] - current_xticks[0]
        ax.set_xlim(
            current_xticks[0] - xtick_range * xpad, current_xticks[-1])
        ax.spines['bottom'].set_bounds(current_xticks[0], current_xticks[-1])
        current_yticks = ax.yaxis.get_ticklocs()
        ytick_range = current_yticks[-1] - current_yticks[0]
        ax.set_ylim(
            current_yticks[0] - ytick_range * ypad, current_yticks[-1])
        ax.spines['left'].set_bounds(current_yticks[0], current_yticks[-1])


def prettify_legend(leg, lw=0, fc='none'):
    """
    Prettify legend (by default, transparent + borderless).

    Parameters
    ----------
    leg: matplotlib.legend.Legend
        legend
    lw : int, optional (default 0)
        bbox line width
    fc : str, optional (default 'none')
        facecolor

    """
    leg.get_frame().set_facecolor(fc)
    leg.get_frame().set_linewidth(lw)



def make_transparent(img_file):
    """
    Make each white pixel in an image transparent.

    Parameters
    ----------
    img_file : str
        absolute path to a PNG image file

    Returns
    -------
    None

    Notes
    -----
    This function overwrites the existing file.

    """
    img = Image.open(img_file)
    img = img.convert("RGBA")
    pixdata: PyAccess.PyAccess = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):  # if white
                pixdata[x, y] = (255, 255, 255, 0)  # set alpha = 0
    img.save(img_file, "PNG")
