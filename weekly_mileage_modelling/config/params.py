"""
Parameters handling
"""

from typing import Annotated

from pydantic import Field, NonNegativeFloat, PositiveFloat
from pydantic_settings import BaseSettings, SettingsConfigDict


class WeeklyMileageParams(BaseSettings):
    """This holds environment variables. Default value has been selected and set."""

    # NOTE: Ensure you have created the .env file in the required place
    # We could also read directly from the env with os.getenv or similar, but I chose a .env file for ease
    model_config = SettingsConfigDict(env_file=".env")

    # NOTE: Added constraint that target & starting mileage should be greater than or equal to 0.
    starting_mileage: NonNegativeFloat = 0
    target_mileage: NonNegativeFloat = 50

    # This validates the a,b fields
    a: Annotated[float, Field(gt=0, lt=1)] = 0.5
    b: PositiveFloat = 0.5

    # NOTE: I added equation choice as an optional parameter in the requests as an alt to using env vars
    # TODO: This is not validated, but it might be a good idea to add validation to ensure the equation_choice
    # appears in the list of valid tags
    equation_choice: str
