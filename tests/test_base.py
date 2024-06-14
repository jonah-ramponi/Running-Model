import pytest
from pydantic import ValidationError

from weekly_mileage_modelling.config.params import WeeklyMileageParams
from weekly_mileage_modelling.models import WeeklyMileageModel


@pytest.fixture
def default_params():
    return WeeklyMileageParams(starting_mileage=10, target_mileage=50, a=0.5, b=3)


@pytest.fixture
def mock_model(default_params):
    return WeeklyMileageModel(params=default_params)


def test_initialization_with_default_params(mock_model):
    assert mock_model.starting_mileage == 10
    assert mock_model.target_mileage == 50
    assert mock_model.a == 0.5
    assert mock_model.b == 3


# This shouldn't be allowed, starting mileage is negative
def test_initialization_with_default_params_invalid_starting_mileage():
    with pytest.raises(ValidationError):
        WeeklyMileageParams(starting_mileage=-10, target_mileage=50, a=0.5, b=0.1)


# This shouldn't be allowed, target mileage is negative
def test_initialization_with_default_params_invalid_target_mileage():
    with pytest.raises(ValidationError):
        WeeklyMileageParams(starting_mileage=10, target_mileage=-50, a=0.5, b=0.1)


# This shouldn't be allowed, a is not s.t. 0 < a < 1
def test_initialization_with_default_params_invalid_a_too_low():
    with pytest.raises(ValidationError):
        WeeklyMileageParams(starting_mileage=10, target_mileage=50, a=0, b=0.1)


# This shouldn't be allowed, a is not s.t. 0 < a < 1
def test_initialization_with_default_params_invalid_a_too_high():
    with pytest.raises(ValidationError):
        WeeklyMileageParams(starting_mileage=10, target_mileage=50, a=1, b=0.1)


# This shouldn't be allowed, b mileage is negative
def test_initialization_with_default_params_invalid_b():
    with pytest.raises(ValidationError):
        WeeklyMileageParams(starting_mileage=10, target_mileage=50, a=1, b=-0.1)


def test_merge_params():
    params = WeeklyMileageParams(starting_mileage=10, target_mileage=50, a=0.5, b=3)

    updated_params = WeeklyMileageModel.merge_params(params, a=0.9)
    assert updated_params.a == 0.9
    assert updated_params.b == 3
    assert updated_params.starting_mileage == 10
    assert updated_params.target_mileage == 50

    updated_params = WeeklyMileageModel.merge_params(params, b=2.5)
    assert updated_params.b == 2.5
    assert updated_params.a == 0.5
    assert updated_params.starting_mileage == 10
    assert updated_params.target_mileage == 50

    updated_params = WeeklyMileageModel.merge_params(params, starting_mileage=20)
    assert updated_params.starting_mileage == 20
    assert updated_params.a == 0.5
    assert updated_params.b == 3
    assert updated_params.target_mileage == 50

    updated_params = WeeklyMileageModel.merge_params(params, target_mileage=60)
    assert updated_params.target_mileage == 60
    assert updated_params.a == 0.5
    assert updated_params.b == 3
    assert updated_params.starting_mileage == 10

    # Test merging with multiple parameters at once
    updated_params = WeeklyMileageModel.merge_params(
        params, a=0.04, b=3, starting_mileage=30, target_mileage=70
    )
    assert updated_params.a == 0.04
    assert updated_params.b == 3
    assert updated_params.starting_mileage == 30
    assert updated_params.target_mileage == 70


def test_update_params(mock_model):
    # Test updating 'a' parameter
    mock_model._update_params(a=0.38)
    assert mock_model.a == 0.38

    # Test updating 'b' parameter
    mock_model._update_params(b=2.5)
    assert mock_model.b == 2.5

    # Test updating 'starting_mileage' parameter
    mock_model._update_params(starting_mileage=20)
    assert mock_model.starting_mileage == 20

    # Test updating 'target_mileage' parameter
    mock_model._update_params(target_mileage=60)
    assert mock_model.target_mileage == 60

    # Test updating multiple parameters at once
    mock_model._update_params(a=0.41, b=3, starting_mileage=30, target_mileage=70)
    assert mock_model.a == 0.41
    assert mock_model.b == 3
    assert mock_model.starting_mileage == 30
    assert mock_model.target_mileage == 70
