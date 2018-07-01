import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation
from math import log

# Image width and height; parameters for the plot
x_res, y_res = 300, 300
xmin, xmax = -1.5, 1.5
width = xmax - xmin
ymin, ymax = -1.5, 1.5
height = ymax - ymin

z_abs_max = 10
max_iter = 1000


def julia_set(c, mkplot=False, savefig=False, cmap="gnuplot2"):
    """
    Returns a matrix of pixel values, and optionally displays a plot
    :param c: the complex seed for the julia set fractal
    :param mkplot: whether to create the plot
    :param cmap: the matplotlib colourmap as a string
    :return: matrix of pixel values
    """
    julia = np.zeros((x_res, y_res))

    for ix in range(x_res):
        for iy in range(y_res):
            # Map pixel position to a point in the complex plane
            z = complex(ix / x_res * width + xmin, iy / y_res * height + ymin)

            # Do the iterations
            iteration = 0
            while abs(z) <= z_abs_max and iteration < max_iter:
                z = z ** 2 + c
                iteration += 1
            iteration_ratio = iteration / max_iter
            julia[ix, iy] = iteration_ratio

    if mkplot:
        fig, ax = plt.subplots()
        ax.imshow(julia, interpolation="nearest", cmap=cm.get_cmap(cmap))
        plt.axis("off")
        plt.show()
        if savefig:
            fig.savefig(f"julia_{c.real}_{c.imag}_{cmap}.png", dpi=800)

    return julia


def julia_animation():
    """
    From a range of real and complex parts, generate julia set images and combine into an animation
    :return: an mp4 animation
    """
    fig, ax = plt.subplots()

    ims = []
    for i in range(-9, 10, 2):
        for j in range(-9, 10, 2):
            c = complex(i / 10, j / 10)
            plt.axis("off")
            julia = julia_set(c, mkplot=False)
            t = ax.annotate(
                f"({round(c.real, 2)}, {round(c.imag, 2)})", (225, 10), color="w"
            )
            plot = ax.imshow(julia, interpolation="nearest", cmap="gnuplot2")
            ims.append((plot, t))

    im_ani = animation.ArtistAnimation(
        fig, ims, interval=300, repeat_delay=3000, blit=True
    )
    im_ani.save("c_choice.mp4", writer=animation.FFMpegWriter())


# Test different cmaps
def julia_cmaps(cmaps_list):
    """
    Displays a number of plots for different cmaps
    :param cmaps_list: a list of matplotlib cmaps to be tested
    :return: individual plots for different cmaps
    """
    for colours in cmaps_list:
        julia_set(complex(-0.1, 0.65), mkplot=True, cmap=colours)


cmaps = [
    "PuOr",
    "RdGy",
    "RdBu",
    "RdYlBu",
    "RdYlGn",
    "Spectral",
    "coolwarm",
    "bwr",
    "seismic",
    "flag",
    "prism",
    "ocean",
    "gist_earth",
    "terrain",
    "gist_stern",
    "gnuplot",
    "gnuplot2",
    "CMRmap",
    "cubehelix",
    "brg",
    "hsv",
    "gist_rainbow",
    "rainbow",
    "jet",
    "nipy_spectral",
    "gist_ncar",
]

julia_cmaps(cmaps)


# Test different complex numbers
x_res = y_res = 300
for i in range(20):
    julia_set(complex(-0.74, -0.1 + i / 200))

fig, ax = plt.subplots()
ims = []
for i in range(20):
    for j in range(10):
        c = complex(-0.6 - j / 100, -0.1 - i / 200)
        plt.axis("off")
        julia = julia_set(c, mkplot=False)
        t = ax.annotate(
            f"({round(c.real, 2)}, {round(c.imag, 2)})", (225, 10), color="w"
        )
        plot = ax.imshow(julia, interpolation="nearest", cmap="gnuplot2")
        ims.append((plot, t))

im_ani = animation.ArtistAnimation(
    fig, ims, interval=500, repeat_delay=3000, blit=True)
im_ani.save("c_choice.mp4", writer=animation.FFMpegWriter())

julia_set(complex(-0.418, -0.59), mkplot=True)
julia_set(complex(-0.593, -0.443), mkplot=True)
julia_set(complex(-0.155, -0.653), mkplot=True)
julia_set(complex(-0.715, -0.225), mkplot=True)
julia_set(complex(-0.705, -0.266), mkplot=True)


# Variants of the Julia set
def julia_set_log(c, base, mkplot=False, savefig=False, cmap="gnuplot2"):
    """
    Returns a matrix of pixel values, and optionally displays a plot
    :param c: the complex seed for the julia set fractal
    :param mkplot: whether to create the plot
    :param cmap: the matplotlib colourmap as a string
    :return: matrix of pixel values
    """
    julia = np.zeros((x_res, y_res))

    for ix in range(x_res):
        for iy in range(y_res):
            # Map pixel position to a point in the complex plane
            z = complex(ix / x_res * width + xmin, iy / y_res * height + ymin)

            # Do the iterations
            iteration = 0
            while abs(z) <= z_abs_max and iteration < max_iter:
                z = z ** 2 + c
                iteration += 1
            iteration_ratio = iteration / max_iter
            # iteration_ratio = iteration / max_iter
            julia[ix, iy] = log(iteration_ratio, base)

    if mkplot:
        fig, ax = plt.subplots()
        ax.imshow(julia, interpolation="nearest", cmap=cm.get_cmap(cmap))
        plt.axis("off")
        plt.show()
        if savefig:
            fig.savefig(f"julia_{c.real}_{c.imag}_{cmap}.png", dpi=800)

    return julia


def julia_set_exp(c, base, mkplot=False, savefig=False, cmap="gnuplot2"):
    """
    Returns a matrix of pixel values, and optionally displays a plot
    :param c: the complex seed for the julia set fractal
    :param base: the base of the log
    :param mkplot: whether to create the plot
    :param cmap: the matplotlib colourmap as a string
    :return: matrix of pixel values
    """
    julia = np.zeros((x_res, y_res))

    for ix in range(x_res):
        for iy in range(y_res):
            # Map pixel position to a point in the complex plane
            z = complex(ix / x_res * width + xmin, iy / y_res * height + ymin)

            # Do the iterations
            iteration = 0
            while abs(z) <= z_abs_max and iteration < max_iter:
                z = z ** 2 + c
                iteration += 1
            # iteration_ratio = np.power(base, iteration/max_iter)

            # iteration_ratio = iteration / max_iter
            julia[ix, iy] = np.power(iteration, base)

    # julia = julia/julia.max()
    if mkplot:
        fig, ax = plt.subplots()
        ax.imshow(julia, interpolation="nearest", cmap=cm.get_cmap(cmap))
        plt.axis("off")
        plt.show()
        if savefig:
            fig.savefig(f"julia_{c.real}_{c.imag}_{cmap}.png", dpi=800)

    return julia


julia_set(complex(-0.715, -0.225), mkplot=True)
julia_set_log(complex(-0.715, -0.225), base=1.001, mkplot=True)

julia_set_exp(complex(-0.715, -0.225), base=1.1, mkplot=True)
julia_set_log(complex(-0.705, -0.266), mkplot=True)
