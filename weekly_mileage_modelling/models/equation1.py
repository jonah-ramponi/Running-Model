"""
Implementation of the first equation
"""

import sympy as sp
from weekly_mileage_modelling.models import WeeklyMileageModel
from weekly_mileage_modelling.config import WeeklyMileageParams


class WeeklyMileageModel1(WeeklyMileageModel):
    """First equation, as defined in part 1 of the task"""

    TAG = "equation1"

    def __init__(self, params: WeeklyMileageParams = None, **kwargs):
        params = self.merge_params(params, **kwargs)
        super().__init__(params)

    def set_equation(self):
        self.equation = sp.Eq(
            self.weekly_mileage,
            self.target_mileage
            - (self.target_mileage - self.starting_mileage)
            * self.a ** (self.n / self.b),
        )
