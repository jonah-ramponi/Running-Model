
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


#### Criticisms

* I have never written unit tests before (and im not a software engineer, nor from a comp sci background), so I am sure what I've done is not best practices. Think that bit could be greatly improved! I did include some comments for Equation1 on derivations of answers, I don't want to spend any more time on this so didn't write them for equation 2. Keen for your criticisms!
* I think the way I handle overwriting args, such as a or b, could be written much better.
* maybe handling default args is better not in env, I think in hindsight it would've been
#### Future Additions

* I think it would be nice if the plans incorporated downtime. Every 4th week @ 90% of the previous weeks mileage. This could be an interesting problem to incorporate, I'd consider using the mod function for this (if n mod 4 == 3, then reduce mileage), either as a multiplier or as an additional term in the equation. 



# rb-modelling-take-home-equation-api

## Background

Consider an equation that determines a runner's `weekly_mileage` for a given week `n` of their training plan:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`weekly_mileage`=`target_mileage`−(`target_mileage`−`starting_mileage`) * `a` ^ (`n`/`b`)

Where:
- `n` is the week number (in the first week `n==0`).
- `target_mileage` is the weekly mileage they would build to, given infinite training time.
- `starting_mileage` is their starting mileage in the first week (`n==0`).
- `a` is a parameter that governs the shape of the curve i.e. how the runner's weekly mileage progresses. 
    - `0 < a < 1`.
- `b` is a parameter that governs the shape of the curve i.e. how the runner's weekly mileage progresses.
    - `b > 0`.

## Task
1. Create a modelling component (up to you what the implementation looks like) that:
    - Enables usage of the above function. Default arguments for `target_mileage`, `starting_mileage`, `a`, `b` should be provided and reused for subsequent inferences, unless overridden.
    - Enables calculating the inverse transform for the same set of variables. I.e. given a value for `weekly_mileage`, with the values set for `target_mileage`, `starting_mileage`, `a`, `b`, return the corresponding value of `n`.
    - Enables calculating the rate of change of the `weekly_mileage` with respect to `n` for a given week. I.e. `d(weekly_mileage)/d(n)` for a given `n`. This can be an approximation or an exact value - please explain your reasoning.
2. Create a new modelling component with the same interface, but for the new equation:
    - `weekly_mileage` = min(`starting_mileage` + (`a` * `n`) / `b`, `target_mileage`)
3. Expose this functionality via a REST API, that enables querying via an http request.
    - There should be 3 end points, one for each of the calculations:
        - The forward transform
        - The reverse transform
        - The rate of change
    - The modelling component to choose (i.e. which base equation to use - either from step 1 or step 2) should depend on an environment variable `EQUATION_CHOICE`.
    - Default arguments for `target_mileage`, `starting_mileage`, `a`, `b` should be read from environment variables, however if custom values are provided in the client request then these should take priority. Here, `n` should always be taken from the client request for the forward transform and the rate of change, and `weekly_mileage` should be taken from the client request for the inverse transform.
4. Please include instructions on how to setup and run the code, and query your endpoints.

## Guidance
- There is very little guidance on implementation here which is intentional - implementation is totally up to you. That said - if anything is unclear, please reach out! Very happy to answer any follow up questions you may have. Send any queries to harry@runna.com.
- Assume all mileages are in `km` - no need to worry about different units here.
- Please write production quality code and treat this task as if you were going to use everything here in a production environment.
- Please detail your thought process (e.g. comments, notes etc).
- Anything you'd like to include/any extensions that you don't have time for, please feel free to leave notes and discussion points for, so we know what you're considering.
- It's up to you how long you spend on this - there are no min/max time constraints. However, we'd like to be respectful of your time so if there's lots more you'd like to add having already invested a reasonable amount of time, please feel free to write what you would do given more time.
