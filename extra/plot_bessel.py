#!/usr/bin/env python
#
# plot_bessel.py --- Generate the plots used in the examples for purdue-beamer
#
# This will work using Python 3. Dependencies are matplotlib, numpy, and scipy
#
# Copyright (c) 2016 Dennis Ogbe <dogbe@purdue.edu>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
from scipy.special import jv
import os
import subprocess
import matplotlib as mpl
mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.markers as mk
import matplotlib.cm as cm


# some housekeeping first
def figsize(scale):
    # Get this from LaTeX by doing:
    # \usepackage{printlen}
    # \printlength\textwidth
    #
    # for IEEEtran: \linewith = 252.0pt, \textwidth is 516.0pt
    fig_width_pt = 252.0
    inches_per_pt = 1.0/72.27
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    aspect_ratio = 12.0/10.0
    # golden_mean = (np.sqrt(5.0)-1.0)/2.0
    # fig_height = fig_width*golden_mean            # height in inches
    fig_height = fig_width * 1/aspect_ratio
    fig_size = [fig_width, fig_height]
    return fig_size


def setup_mpl():
    # set up matplotlib to use TeX and to use the IEEEtran fonts
    # http://matplotlib.org/users/usetex.html
    # more info on settings here:
    # http://matplotlib.org/users/customizing.html#customizing-matplotlib
    # http://bkanuka.com/articles/native-latex-plots/
    pgf_with_latex = {
        # change this if using xetex or luatex
        "pgf.texsystem": "pdflatex",
        # use LaTeX to write all text
        "text.usetex": True,
        # choose the font family
        "font.family": "sans-serif",
        # blank entries should cause plots to inherit fonts from the document
        # otherwise, for IEEEtran we have the following:
        # "font.serif": ["Times"],
        # "font.sans-serif": ["Helvetica"],
        # "font.monospace": ["Courier"],
        "font.serif": [],
        "font.sans-serif": [],
        "font.monospace": [],
        # set sizes [pt]. LaTeX/IEEEtran default is 10pt
        "axes.labelsize": 10,
        "font.size": 10,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        # default fig size of 1 fig_width_pt (see figsize() function)
        "figure.figsize": figsize(1),
        # plots will be generated using this preamble
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
        ]
    }
    mpl.rcParams.update(pgf_with_latex)


# save the figure in the output directories
def save_figure(fig, name, open_preview=False):
    # use figure in LaTeX by doing:
    # \input{file.pgf}
    # fig.tight_layout(pad=0)
    fig.tight_layout()
    basedir = os.path.abspath("..")
    pgfnames = ["{}/{}.pgf".format("/".join([basedir, gw, "plots"]), name)
                for gw in ["gold", "white"]]
    pdfnames = ["{}/{}.pdf".format("/".join([basedir, gw, "plots"]), name)
                for gw in ["gold", "white"]]
    # save the output as PGF/TikZ file
    for f in pgfnames:
        fig.savefig(f, format="pgf")
    # save copy as pdf the preview
    for f in pdfnames:
        fig.savefig(f, format="pdf", dpi=300)
    # open pdf file to preview
    if open_preview:
        subprocess.Popen(["evince", pdfnames[0]],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.STDOUT)


# can use code like this to produce a plot. alternatively, we could load some
# data computed in MATLAB, Julia or something along those lines using csv,
# json, of hdf5.
def plot_functions():
    # instantiate figure and axes objects
    fig, ax = plt.subplots()

    # we want to plot a few Bessel functions over the interval (0, 20)
    x = np.linspace(0, 15, 10000)
    vs = np.arange(6)

    # define some line widths
    lwidth = 1.5
    gwidth = 0.5
    bwidth = 0.5

    # the line styles
    nlines = len(vs)
    colormap = cm.viridis
    colors = [colormap(x) for x in np.linspace(0.0, 1.0, nlines)]
    # we could also do something along the lines of
    # colors = ["blue", "red", "yellow", "purple", "green"]
    linestyles = ["solid", "dashed"] * int(nlines//2)

    # the marker styles -- optional, disabled for these plots
    # markerstyles = mk.MarkerStyle.filled_markers
    markerstyles = [None] * nlines
    markeredgecolors = colors
    markerfacecolors = colors
    markersizes = [3] * nlines
    markeredgewidths = [lwidth] * nlines
    markersizes = [4] * nlines
    marker_int = 1000

    # loop and plot the function
    for i, v in enumerate(vs):
        style = {
            # we can use TeX formatting for the legend labels
            "label": r"$J_{{{:d}}}(x)$".format(v),

            # color and line style
            "color": colors[i],
            "linestyle": linestyles[i],
            "linewidth": lwidth,

            # current marker
            "marker": markerstyles[i],
            "markevery": marker_int,
            "markeredgecolor": markeredgecolors[i],
            "markerfacecolor": markerfacecolors[i],
            "markersize": markersizes[i],
            "markeredgewidth": markeredgewidths[i],

            # this is -- of course -- all optional
            "dash_capstyle": "butt",
            "solid_capstyle": "butt",
            "dash_joinstyle": "miter",
            "solid_joinstyle": "miter",
        }

        # compute the data points and plot the line
        y = jv(v, x)
        ax.plot(x, y, **style)

    # limits
    ax.set_xlim((x[0], x[-1]))

    # labels
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$J_{n}(x)$")

    # grid
    ax.grid(linewidth=gwidth,
            alpha=0.6,
            color="gray",
            linestyle="solid")

    # legend
    leg = ax.legend(loc=0,
                    labelspacing=0.2,
                    borderpad=0.2,
                    handletextpad=0.2)
    leg.get_frame().set_linewidth(bwidth)

    # spines (the "borders" of the axes)
    for _, spine in ax.spines.items():
        spine.set_linewidth(bwidth)

    # save the figure
    save_figure(fig, "bessel", open_preview=True)


# a QnD main function
def main():
    setup_mpl()
    plot_functions()


if __name__ == '__main__':
    main()
