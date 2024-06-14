
#### Setup
```
conda create -n weekly_mileage_model python=3.11

conda activate weekly_mileage_model

python -m pip install -r requirements.txt

# Create .env, based on the template provided in .env.example (you could just rename .env.example)

python main.py

# To view the quick interface I used for visualising the equations,
# It will be accessible by default at localhost:8501, if you are on a remote machine ensure you portforward the required port. 
```

#### Notes
* Setup to accept optional tag for equation in request, if you wish to pass it instead of switching between env vars
* will read from .env, NOT the environment directly in this version.
* used sympy for the math stuff, which should make this easier to extend to other models

#### Equation 2 derivative 

As Equation 2 is Piecewise, and therefore not necessarily continuous, we need to evaluate the derivative at the inequality (potentially point of discontinuity).


weekly_{mileage} = \begin{cases} s_m + \frac{an}{b} & \text{for}\: s_m + \frac{an}{b} \leq t_m \\ t_m & \text{otherwise} \end{cases}


LHS derivative at s_m + \frac{an}{b} = t_m:

\frac{d}{dn} = \frac{a}{b}

RHS derivative at s_m + \frac{an}{b} = t_m:

\frac{d}{dn} = 0 

The derivatives do not match, therefore the function is not differentiable at the equality and therefore the derivative should be undefined. 


#### Criticisms

* I have never written unit tests before, so I am sure what I've done is not best practices. Think that bit could be greatly improved! I did include some comments for Equation1 on derivations of answers, I don't want to spend any more time on this so didn't write them for equation 2. 
* I think the way I handle overwriting args, such as a or b, could be written much better.
* I think setting up with pydantic-settings reading from .env may not be what was expected.

#### Future Additions

* I think it would be nice if the plans incorporated downtime. Every 4th week @ 90% of the previous weeks mileage. This could be an interesting problem to incorporate, I'd consider using the mod function for this (if n mod 4 == 3, then reduce mileage), either as a multiplier or as an additional term in the equation. 

* 