"""Control chart calculations for SPC dashboard."""

from __future__ import annotations

import numpy as np

from src.spc_engine.constants import IMR_D2, IMR_D4, IMR_E2, XBAR_R_CONSTANTS, XBAR_S_CONSTANTS


def compute_xbar_r(subgroups: list[list[float]]) -> dict[str, float | list[float]]:
    subgroup_array = _validate_subgroups(subgroups)
    subgroup_size = subgroup_array.shape[1]
    if subgroup_size not in XBAR_R_CONSTANTS:
        raise ValueError("X-bar R chart requires subgroup size between 2 and 10.")

    constants = XBAR_R_CONSTANTS[subgroup_size]
    subgroup_means = subgroup_array.mean(axis=1)
    ranges = subgroup_array.max(axis=1) - subgroup_array.min(axis=1)
    xbarbar = float(subgroup_means.mean())
    rbar = float(ranges.mean())

    return {
        "subgroup_means": subgroup_means.tolist(),
        "ranges": ranges.tolist(),
        "xbarbar": xbarbar,
        "rbar": rbar,
        "ucl_x": xbarbar + (constants["A2"] * rbar),
        "lcl_x": xbarbar - (constants["A2"] * rbar),
        "ucl_r": constants["D4"] * rbar,
        "lcl_r": max(0.0, constants["D3"] * rbar),
        "sigma_hat": rbar / constants["d2"],
    }


def compute_xbar_s(subgroups: list[list[float]]) -> dict[str, float | list[float]]:
    subgroup_array = _validate_subgroups(subgroups)
    subgroup_size = subgroup_array.shape[1]
    if subgroup_size not in XBAR_S_CONSTANTS:
        raise ValueError("X-bar S chart requires subgroup size between 2 and 12.")

    constants = XBAR_S_CONSTANTS[subgroup_size]
    subgroup_means = subgroup_array.mean(axis=1)
    std_devs = subgroup_array.std(axis=1, ddof=1)
    xbarbar = float(subgroup_means.mean())
    sbar = float(std_devs.mean())

    return {
        "subgroup_means": subgroup_means.tolist(),
        "std_devs": std_devs.tolist(),
        "xbarbar": xbarbar,
        "sbar": sbar,
        "ucl_x": xbarbar + (constants["A3"] * sbar),
        "lcl_x": xbarbar - (constants["A3"] * sbar),
        "ucl_s": constants["B4"] * sbar,
        "lcl_s": max(0.0, constants["B3"] * sbar),
        "sigma_hat": sbar / constants["c4"],
    }


def compute_imr(values: list[float]) -> dict[str, float | list[float]]:
    values_array = np.asarray(values, dtype=float)
    if values_array.ndim != 1 or values_array.size < 2:
        raise ValueError("I-MR chart requires at least two values.")

    moving_ranges = np.abs(np.diff(values_array))
    xbar = float(values_array.mean())
    mrbar = float(moving_ranges.mean())

    return {
        "values": values_array.tolist(),
        "moving_ranges": moving_ranges.tolist(),
        "xbar": xbar,
        "mrbar": mrbar,
        "ucl_x": xbar + (IMR_E2 * mrbar),
        "lcl_x": xbar - (IMR_E2 * mrbar),
        "ucl_mr": IMR_D4 * mrbar,
        "lcl_mr": 0.0,
        "sigma_hat": mrbar / IMR_D2,
    }


def _validate_subgroups(subgroups: list[list[float]]) -> np.ndarray:
    subgroup_array = np.asarray(subgroups, dtype=float)
    if subgroup_array.ndim != 2 or subgroup_array.shape[0] == 0:
        raise ValueError("Control chart input must be a 2D subgroup array.")
    return subgroup_array
