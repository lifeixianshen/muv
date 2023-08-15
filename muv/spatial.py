"""
Spatial statistics.
"""

__author__ = "Steven Kearnes"
__copyright__ = "Copyright 2014, Stanford University"
__license__ = "3-clause BSD"

import numpy as np
from scipy.spatial.distance import cdist, is_valid_dm


def distance(a, b):
    """
    Calculate pairwise distances between examples in two datasets.

    Parameters
    ----------
    a, b : ndarray
        Descriptor datasets with examples on the first axis and descriptors
        on the second axis.
    """
    return cdist(a, b)


def spread(d, t):
    """
    Calculate the spread between two sets of compounds.

    Given a matrix containing distances between two sets of compounds, A
    and B, calculate the fraction of compounds in set A that are closer
    than t to any compound in set B.

    If the distance matrix is symmetric and has zero diagonals, the
    diagonal values are ignored.

    Parameters
    ----------
    d : ndarray
        Distance matrix with compounds from set A on first axis.
    t : float
        Distance threshold.
    """

    # test for symmetric distance matrix
    # diagonal values should be ignored
    if is_valid_dm(d):
        d = np.copy(d)
        d[np.diag_indices_from(d)] = np.inf
    return np.mean(np.any(d < t, axis=1))


def sum_of_spreads(d, coeff, min_t=0, max_t=3, step=None, diff=None):
    """
    Calculate the sum of spreads (or spread differences) across a range of
    distance thresholds.

    Parameters
    ----------
    d : ndarray
        Distance matrix.
    coeff : float
        Coefficient used to rescale distance thresholds.
    min_t : float, optional (default 0)
        Minimum distance threshold (before rescaling).
    max_t : float, optional (default 3)
        Maximum distance threshold (before rescaling).
    step : float, optional
        Step size for determining values to sample between min_t and max_t.
        If not provided, defaults to max_t / 500.
    diff : ndarray, optional
        Distance matrix. If provided, the spread will be calculated for this
        distance matrix and subtracted from the spread of d at each distance
        threshold.
    """
    if step is None:
        step = max_t / 500.
    n_steps = int((max_t - min_t) / step)
    thresholds = coeff * np.linspace(min_t, max_t, n_steps)
    return (
        np.sum([spread(d, t) - spread(diff, t) for t in thresholds])
        if diff is not None
        else np.sum([spread(d, t) for t in thresholds])
    )
