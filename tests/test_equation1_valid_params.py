"""
Example test to ensure the values work out to the correct ones
"""

import pytest

from weekly_mileage_modelling.models.equation1 import WeeklyMileageModel1
from weekly_mileage_modelling.config.params import WeeklyMileageParams


@pytest.fixture
def mock_params():
    return WeeklyMileageParams(starting_mileage=10.0, target_mileage=30.0, a=0.7, b=2.0)


@pytest.fixture
def mock_model(mock_params):
    return WeeklyMileageModel1(params=mock_params)


# just plugged in the numbers
def test_forward_transform(mock_model):
    result = mock_model.forward_transform(n=10)

    assert result == pytest.approx(26.63, rel=1e-2)


# y = t - (t - s)*a^(n/b)
# 15 = 30 - (30 - 10)*0.7^(n/2)
# 15/20 = 0.7^(n/2)
# log(0.75)/log(0.7)*2 = n
# n = 1.61
def test_inverse_transform(mock_model):
    result = mock_model.inverse_transform(weekly_mileage_value=15.0)

    assert result == pytest.approx(1.61, rel=1e-2)


# y = t - (t - s)*a^(n/b)
# dy/dn = -(t-s) dy/dn(a^(n/b))
# dy/dn = -20 * ...

# chain rule
# dy/dn of 0.7^(n/2) = 0.7**(n/2) *ln(0.7)/2
# with inner f_i: u = n/b, outer f_o: f(u) =a^u giving f_o = a^uln(a) and f_i 1/b
# -20 * 0.7**(5/2) *ln(0.7)/2 = 1.4622


def test_rate_of_change_with_respect_to_n(mock_model):
    result = mock_model.rate_of_change_with_respect_to_n(n_value=5)

    assert result == pytest.approx(1.46, rel=1e-2)
