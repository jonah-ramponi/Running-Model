import pytest

from weekly_mileage_modelling.models.equation1 import WeeklyMileageModel1
from weekly_mileage_modelling.config.params import WeeklyMileageParams


@pytest.fixture
def mock_params():
    return WeeklyMileageParams(starting_mileage=10.0, target_mileage=30.0, a=0.7, b=2.0)


@pytest.fixture
def mock_model(mock_params):
    return WeeklyMileageModel1(params=mock_params)


# n is negative, thus a ValueError should be raised
def test_forward_transform(mock_model):
    with pytest.raises(ValueError):
        mock_model.forward_transform(n=-1)


# The plan mileage will never hit 55, with a target mileage of 30, so a value error should be raised
def test_inverse_transform(mock_model):
    with pytest.raises(ValueError):
        mock_model.inverse_transform(weekly_mileage_value=55.0)


# n is negative, thus a ValueError should be raised
def test_rate_of_change_with_respect_to_n(mock_model):
    with pytest.raises(ValueError):
        mock_model.rate_of_change_with_respect_to_n(n_value=-5)
