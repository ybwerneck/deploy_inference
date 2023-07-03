"""Screened Poisson Distance 
Equation taken from,
https://www.researchgate.net/publication/266149392_Dynamic_Distance-Based_Shape_Features_for_Gait_Recognition,
Equation 6 in paper.
"""

from sympy import Symbol, Function, sqrt

from modulus.eq.pde import PDE


class ScreenedPoissonDistance(PDE):
    """
    Screened Poisson Distance

    Parameters
    ==========
    distance : str
        A user-defined variable for distance.
        Default is "normal_distance".
    tau : float
        A small, positive parameter. Default is 0.1.
    dim : int
        Dimension of the Screened Poisson Distance (1, 2, or 3).
        Default is 3.

    Example
    ========
    >>> s = ScreenedPoissonDistance(tau=0.1, dim=2)
    >>> s.pprint()
      screened_poisson_normal_distance: -normal_distance__x**2
      + 0.316227766016838*normal_distance__x__x - normal_distance__y**2
      + 0.316227766016838*normal_distance__y__y + 1
    """

    name = "ScreenedPoissonDistance"

    def __init__(self, distance="normal_distance", tau=0.1, dim=3):
        # set params
        self.distance = distance
        self.dim = dim

        # coordinates
        x, y, z = Symbol("x"), Symbol("y"), Symbol("z")

        # make input variables
        input_variables = {"x": x, "y": y, "z": z}
        if self.dim == 1:
            input_variables.pop("y")
            input_variables.pop("z")
        elif self.dim == 2:
            input_variables.pop("z")

        # distance u
        assert type(distance) == str, "distance needs to be string"
        distance = Function(distance)(*input_variables)

        # set equations
        self.equations = {}
        sdf_grad = (
            1 - distance.diff(x) ** 2 - distance.diff(y) ** 2 - distance.diff(z) ** 2
        )
        poisson = sqrt(tau) * (
            distance.diff(x, 2) + distance.diff(y, 2) + distance.diff(z, 2)
        )
        self.equations["screened_poisson_" + self.distance] = sdf_grad + poisson
