"""
Example test to ensure the values work out to the correct ones
"""

import pytest
import numpy as np

from weekly_mileage_modelling.models.equation2 import WeeklyMileageModel2
from weekly_mileage_modelling.config.params import WeeklyMileageParams


@pytest.fixture
def mock_params():
    return WeeklyMileageParams(starting_mileage=20.0, target_mileage=30.0, a=0.5, b=1.0)


@pytest.fixture
def mock_model(mock_params):
    return WeeklyMileageModel2(params=mock_params)


# Should return float("nan"), I chose not to make this return a value error but maybe that would be better for consistency.
def test_rate_of_change_with_respect_to_n(mock_model):
    result = mock_model.rate_of_change_with_respect_to_n(n_value=20)
    assert np.isnan(result)
