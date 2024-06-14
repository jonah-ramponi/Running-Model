"""
Implementation of the 2nd Equation
"""

import sympy as sp
from weekly_mileage_modelling.models import WeeklyMileageModel
from weekly_mileage_modelling.config import WeeklyMileageParams


class WeeklyMileageModel2(WeeklyMileageModel):
    """Second Equation, defined in part 2 of the Task"""

    TAG = "equation2"

    def __init__(self, params: WeeklyMileageParams = None, **kwargs):
        params = self.merge_params(params, **kwargs)
        super().__init__(params)

    def set_equation(self):
        condition = (
            self.starting_mileage + self.a * self.n / self.b <= self.target_mileage
        )

        self.equation = sp.Eq(
            self.weekly_mileage,
            sp.Piecewise(
                (self.starting_mileage + self.a * self.n / self.b, condition),
                (
                    self.target_mileage,
                    ~condition,
                ),  # ~condition is the negation of the condition
            ),
        )
