
import numpy
import math
import matplotlib.pyplot as plt
import scipy.special
from scipy.special import sph_harm
import warnings
warnings.filterwarnings("ignore")


def hydrogen_wf(n, l, m, X, Y, Z):
    R = numpy.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    Theta = numpy.arccos(Z / R)
    Phi = numpy.arctan2(Y, X)

    rho = 2. * R / n
    s_harm = sph_harm(m, l, Phi, Theta)
    l_poly = scipy.special.genlaguerre(n - l - 1, 2 * l + 1)(rho)

    prefactor = numpy.sqrt((2. / n) ** 3 * math.factorial(n - l - 1) / (2. * n * math.factorial(n + l)))
    wf = prefactor * numpy.exp(-rho / 2.) * rho ** l * s_harm * l_poly
    wf = numpy.nan_to_num(wf)
    return wf


def create_hydrogen(n, l, m, ax):
    dz = 0.5
    zmin = -10
    zmax = 10
    x = numpy.arange(zmin, zmax, dz)
    y = numpy.arange(zmin, zmax, dz)
    z = numpy.arange(zmin, zmax, dz)
    X, Y, Z = numpy.meshgrid(x, y,z)

    data = hydrogen_wf(n, l, m, X, Y, Z)
    data = abs(data) ** 2

    plt.subplots_adjust(left=-0.1, bottom=0.1)
    im = plt.imshow(data[int((0 - zmin) / dz), :, :], vmin=0, vmax=numpy.max(data), extent=[zmin, zmax, zmin, zmax])
    plt.colorbar()

    ax.set_title(
        "Hydrogen Orbital xz Slice (y=0): n=" + str(n) + ", l=" + str(
            l) + ", m=" + str(m))

    return im, data



