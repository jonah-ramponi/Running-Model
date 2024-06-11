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
    - The modelling component to choose (i.e. which base equation to use) should depend on an environment variable `EQUATION_CHOICE`.
    - Default arguments for `target_mileage`, `starting_mileage`, `a`, `b` should be read from environment variables, however if custom values are provided in the client request then these should take priority. Here, `n` should always be taken from the client request for the forward transform and the rate of change, and `weekly_mileage` should be taken from the client request for the inverse transform.
4. Please include instructions on how to setup and run the code, and query your endpoints.

## Guidance
- There is very little guidance on implementation here which is intentional - implementation is totally up to you. That said - if anything is unclear, please reach out! Very happy to answer any follow up questions you may have. Send any queries to harry@runna.com.
- Assume all mileages are in `km` - no need to worry about different units here.
- Please write production quality code and treat this task as if you were going to use everything here in a production environment.
- Please detail your thought process (e.g. comments, notes etc).
- Anything you'd like to include/any extensions that you don't have time for, please feel free to leave notes and discussion points for, so we know what you're considering.
- It's up to you how long you spend on this - there are no min/max time constraints. However, we'd like to be respectful of your time so if there's lots more you'd like to add having already invested a reasonable amount of time, please feel free to write what you would do given more time.
