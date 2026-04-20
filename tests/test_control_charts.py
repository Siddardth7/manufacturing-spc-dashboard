import math

import pytest

from src.spc_engine.control_charts import compute_imr, compute_xbar_r, compute_xbar_s


XBAR_R_SAMPLE = [
    [10, 11, 12, 13, 14],
    [11, 12, 13, 14, 15],
    [9, 10, 11, 12, 13],
]

XBAR_S_SAMPLE = [
    list(range(1, 13)),
    list(range(2, 14)),
    list(range(3, 15)),
]

IMR_SAMPLE = [10, 12, 11, 15, 14]


def test_compute_xbar_r_returns_expected_keys():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    expected = {
        "subgroup_means",
        "ranges",
        "xbarbar",
        "rbar",
        "ucl_x",
        "lcl_x",
        "ucl_r",
        "lcl_r",
        "sigma_hat",
    }
    assert expected.issubset(result.keys())


def test_compute_xbar_r_subgroup_means():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["subgroup_means"] == pytest.approx([12.0, 13.0, 11.0])


def test_compute_xbar_r_ranges():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["ranges"] == pytest.approx([4.0, 4.0, 4.0])


def test_compute_xbar_r_xbar_limits_use_aiag_a2_for_n5():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["ucl_x"] == pytest.approx(14.308, rel=1e-4)
    assert result["lcl_x"] == pytest.approx(9.692, rel=1e-4)


def test_compute_xbar_r_r_limits_use_aiag_d4_for_n5():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["ucl_r"] == pytest.approx(8.456, rel=1e-4)


def test_compute_xbar_r_lcl_r_clamped_at_zero():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["lcl_r"] == pytest.approx(0.0)


def test_compute_xbar_r_sigma_hat_uses_d2():
    result = compute_xbar_r(XBAR_R_SAMPLE)
    assert result["sigma_hat"] == pytest.approx(4.0 / 2.326, rel=1e-4)


def test_compute_xbar_r_invalid_n_raises():
    with pytest.raises(ValueError):
        compute_xbar_r([[1], [2], [3]])


def test_compute_xbar_s_returns_expected_keys():
    result = compute_xbar_s(XBAR_S_SAMPLE)
    expected = {
        "subgroup_means",
        "std_devs",
        "xbarbar",
        "sbar",
        "ucl_x",
        "lcl_x",
        "ucl_s",
        "lcl_s",
        "sigma_hat",
    }
    assert expected.issubset(result.keys())


def test_compute_xbar_s_ucl_formula_for_n12():
    result = compute_xbar_s(XBAR_S_SAMPLE)
    subgroup_std = math.sqrt(13.0)
    expected_ucl = 7.5 + (0.886 * subgroup_std)
    assert result["ucl_x"] == pytest.approx(expected_ucl, rel=1e-4)


def test_compute_xbar_s_sigma_hat_uses_c4():
    result = compute_xbar_s(XBAR_S_SAMPLE)
    subgroup_std = math.sqrt(13.0)
    assert result["sigma_hat"] == pytest.approx(subgroup_std / 0.9776, rel=1e-4)


def test_compute_imr_returns_expected_keys():
    result = compute_imr(IMR_SAMPLE)
    expected = {
        "values",
        "moving_ranges",
        "xbar",
        "mrbar",
        "ucl_x",
        "lcl_x",
        "ucl_mr",
        "lcl_mr",
        "sigma_hat",
    }
    assert expected.issubset(result.keys())


def test_compute_imr_moving_ranges():
    result = compute_imr(IMR_SAMPLE)
    assert result["moving_ranges"] == pytest.approx([2.0, 1.0, 4.0, 1.0])


def test_compute_imr_x_limits_use_e2():
    result = compute_imr(IMR_SAMPLE)
    assert result["ucl_x"] == pytest.approx(17.72, rel=1e-4)
    assert result["lcl_x"] == pytest.approx(7.08, rel=1e-4)


def test_compute_imr_mr_limits_use_d4():
    result = compute_imr(IMR_SAMPLE)
    assert result["ucl_mr"] == pytest.approx(6.534, rel=1e-4)


def test_compute_imr_sigma_hat_uses_d2():
    result = compute_imr(IMR_SAMPLE)
    assert result["sigma_hat"] == pytest.approx(2.0 / 1.128, rel=1e-4)
