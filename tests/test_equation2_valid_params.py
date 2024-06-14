"""
Example test to ensure the values work out to the correct ones
"""

import pytest

from weekly_mileage_modelling.models.equation2 import WeeklyMileageModel2
from weekly_mileage_modelling.config.params import WeeklyMileageParams


@pytest.fixture
def mock_params():
    return WeeklyMileageParams(starting_mileage=10.0, target_mileage=30.0, a=0.7, b=2.0)


@pytest.fixture
def mock_model(mock_params):
    return WeeklyMileageModel2(params=mock_params)


def test_forward_transform(mock_model):
    result = mock_model.forward_transform(n=10)

    assert result == pytest.approx(13.5, rel=1e-2)


def test_inverse_transform(mock_model):
    result = mock_model.inverse_transform(weekly_mileage_value=15.0)

    assert result == pytest.approx(14.29, rel=1e-2)


def test_rate_of_change_with_respect_to_n(mock_model):
    result = mock_model.rate_of_change_with_respect_to_n(n_value=5)

    assert result == pytest.approx(0.35, rel=1e-2)
