
#### Setup
```
conda create -n jonahs_env python=3.11

conda activate jonahs_env

python -m pip install -r requirements.txt

pip install .

# Create .env, based on the template provided in .env.example (you could just rename .env.example)
# you can then set env vars with
python scripts/set_env.py

python weekly_mileage_modelling/api/run.py --port 8000
python -m streamlit run frontend/interface.py --server.port 8501

# To view the quick interface I used for visualising the equations,
# It will be accessible by default at localhost:8501, if you are on a remote machine ensure you portforward the required port. 
```

#### Notes
* Setup to accept optional tag for equation in request, if you wish to pass it instead of switching between env vars
* used sympy for the math stuff, which should make this easier to extend to other models
* under scripts/example_api_request.py you can see some examples to make calls. To make a call you must first run the api, which I do via python python weekly_mileage_modelling/api/run.py --port 8000
* see github workflow for how I naively set env vars

#### Equation 2 derivative 

As Equation 2 is Piecewise, and therefore not necessarily continuous, we need to evaluate the derivative at the inequality (potentially point of discontinuity).


weekly_{mileage} = \begin{cases} s_m + \frac{an}{b} & \text{for}\: s_m + \frac{an}{b} \leq t_m \\ t_m & \text{otherwise} \end{cases}


LHS derivative at s_m + \frac{an}{b} = t_m:

\frac{d}{dn} = \frac{a}{b}

RHS derivative at s_m + \frac{an}{b} = t_m:

\frac{d}{dn} = 0 

The derivatives do not match, therefore the function is not differentiable at the equality and therefore the derivative should be undefined. 
