import sympy as sp

from weekly_mileage_modelling.config.params import WeeklyMileageParams


class WeeklyMileageModel:
    """Base model to construct different weekly_mileage models from"""

    def __init__(self, params: WeeklyMileageParams = None):
        self.params = params or WeeklyMileageParams()
        self.starting_mileage = params.starting_mileage
        self.target_mileage = params.target_mileage
        self.a = params.a
        self.b = params.b
        self.weekly_mileage = sp.symbols("weekly_mileage")
        self.n = sp.symbols("n")

        self._equation_is_set = False
        self.equation = None

    def __str__(self):
        """Sets str repr to equation in LaTeX format"""
        self._ensure_equation_is_set()
        return sp.latex(self.equation)

    def set_equation(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def _ensure_equation_is_set(self):
        """Function to check an equation has been set"""
        if not self._equation_is_set:
            self.set_equation()
            self._equation_is_set = True

    def forward_transform(self, n: int, **kwargs) -> float:
        """Calculate the forward transform, solving for weekly_mileage given n"""
        if n < 0:
            raise ValueError("You must pick a positive value for the week (n)")

        self._update_params(**kwargs)

        self._ensure_equation_is_set()

        weekly_mileage_value = sp.solve(
            self.equation.subs(self.n, n), self.weekly_mileage
        )[0]

        return weekly_mileage_value

    def inverse_transform(self, weekly_mileage_value: float, **kwargs) -> float:
        """Invert the given function, solving for n and then substitute the entered weekly_mileage_value"""
        if weekly_mileage_value < 0:
            raise ValueError(
                "You must pick a positive value for the weekly mileage (weekly_mileage_value)"
            )

        self._update_params(**kwargs)
        self._ensure_equation_is_set()

        # solve equation for n
        inverted_f = sp.solve(self.equation, self.n)

        # substitute weekly_mileage_value into re-arrange eq
        n_value = inverted_f[0].subs(self.weekly_mileage, weekly_mileage_value)

        # Check for imaginary terms, in which case I choose to raise ValueError
        if any(term.has(sp.I) for term in n_value.as_ordered_terms()):
            raise ValueError(
                f"The solution for n is imaginary. Cannot compute inverse transform evaluated at {weekly_mileage_value}."
            )

        return n_value

    def rate_of_change_with_respect_to_n(self, n_value: int, **kwargs) -> float:
        """Take the derivative of the equation w.r.t n, then substitute for n to return the derivative evaluated at n"""
        if n_value < 0:
            raise ValueError("You must pick a positive value for the week (n)")

        self._update_params(**kwargs)
        self._ensure_equation_is_set()

        # take the derivative, then substitute the value of n the user gave
        # NOTE: Derivate for Equation (2) should be undefined, see Readme.
        # sympy differentiation seems surprisingly poorly documented on piecewise functions,
        # https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html
        # https://github.com/sympy/sympy/issues/11402 suggests that the derivative may be evaluated
        # at the equality (e.g. f(n) = s_m + (an)/b -> d/dn = a/b).
        # With more time I'd properly evaluate how suitable Sympy as as a solver.
        derivative = sp.diff(self.equation.rhs, self.n).subs(self.n, n_value)

        # For now, I wrote a simple check to see if we are at the point which is not differentiable
        epsilon = 1e-9  # add a precision level to compensate for fp precision issues
        if (
            abs(
                self.starting_mileage
                + (self.a * n_value) / self.b
                - self.target_mileage
            )
            < epsilon
            and self.TAG == "equation2"
        ):
            return float("nan")

        return derivative

    def _update_params(self, **kwargs):
        """Update parameters based on kwargs"""
        updated_params = self.merge_params(self.params, **kwargs)
        self.params = updated_params

        if "a" in kwargs:
            self.a = kwargs["a"]
        if "b" in kwargs:
            self.b = kwargs["b"]
        if "starting_mileage" in kwargs:
            self.starting_mileage = kwargs["starting_mileage"]
        if "target_mileage" in kwargs:
            self.target_mileage = kwargs["target_mileage"]

    @staticmethod
    def merge_params(
        params: WeeklyMileageParams = None, **kwargs
    ) -> WeeklyMileageParams:
        """This enables kwargs to be passed to subclasses, and used in the WeeklyMileageParams dataclass"""
        if params is None:
            params = WeeklyMileageParams()

        # Update the default params with provided kwargs
        params_dict = params.dict()
        params_dict.update(kwargs)

        # Return a new instance of WeeklyMileageParams with updated values
        return WeeklyMileageParams(**params_dict)
