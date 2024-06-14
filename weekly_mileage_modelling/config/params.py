"""
Parameters handling
"""

import os
from typing import Annotated

from pydantic import Field, NonNegativeFloat, PositiveFloat, BaseModel


class WeeklyMileageParams(BaseModel):
    """This holds environment variables. Default value has been selected and set."""

    starting_mileage: NonNegativeFloat = os.getenv("STARTING_MILEAGE", default=0)
    target_mileage: NonNegativeFloat = os.getenv("TARGET_MILEAGE", default=50)

    # This validates the a,b fields
    a: Annotated[float, Field(gt=0, lt=1)] = os.getenv("A", default=0.5)
    b: PositiveFloat = os.getenv("B", default=0.5)

    # NOTE: I added equation choice as an optional parameter in the requests as an alt to using env vars
    # TODO: This is not validated, but it might be a good idea to add validation to ensure the equation_choice
    # appears in the list of valid tags
    equation_choice: str
