"""
Script to run the api
"""

import os
import argparse

import uvicorn
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

from weekly_mileage_modelling.models import (
    WeeklyMileageModel1,
    WeeklyMileageModel2,
)

# Suggested in https://github.com/tiangolo/fastapi/discussions/8029, to handle 'nan' being passed in FastAPI request
app = FastAPI(default_response_class=ORJSONResponse)
test_client = TestClient(app)

models = [
    WeeklyMileageModel1,
    WeeklyMileageModel2,
]


def get_selected_model(tag: str):
    """Match selected tag to model tags"""
    for model in models:
        if hasattr(model, "TAG") and model.TAG == tag:
            return model()

    raise ValueError(
        "The provided tag was not associated with a model. Please use a valid model tag."
    )


# Base request model for shared parameters
class BaseTransformRequest(BaseModel):
    """These are optional parameters for requests. If not entered, env vars will be used."""

    a: Optional[float] = None
    b: Optional[float] = None

    starting_mileage: Optional[float] = None
    target_mileage: Optional[float] = None
    equation_choice: Optional[str] = None


# These are used to ensure the required parameters are passed in the request, while also allowing the user to pass optional arguments if they wish to override defaults
class ForwardTransformRequest(BaseTransformRequest):
    n: int


class ReverseTransformRequest(BaseTransformRequest):
    weekly_mileage: float


class RateOfChangeRequest(BaseTransformRequest):
    n: int


# Function to load the appropriate equation model
def load_equation_model(equation_choice: str = None):

    # This loads in the default model
    if equation_choice:
        return get_selected_model(equation_choice)

    # If we did not get equation_choice set in the request, default to env.
    equation_choice_default = os.getenv("EQUATION_CHOICE", "equation1")

    return get_selected_model(equation_choice_default)


def update_equation_params(params: BaseTransformRequest):
    """Takes a request, and passes on the parameters to the equation instance"""

    request_params = params.model_dump()

    # If user passes equation_choice we will use it
    equation_instance = load_equation_model(request_params.get("equation_choice", None))

    # Pydantic validator requires only the keys defined in the model to be passed, thus
    # we need to know which keys we will update. This should really be cached so it is not
    # recomputed every time.
    valid_keys = BaseTransformRequest.model_fields.keys()

    update_kwargs = {
        k: v for k, v in request_params.items() if k in valid_keys and v is not None
    }

    # update the required keys for the equation instance
    equation_instance._update_params(**update_kwargs)

    return equation_instance


# Endpoint for forward transform
@app.post("/forward-transform")
async def forward_transform(request: ForwardTransformRequest) -> Dict[str, float]:
    equation_instance = update_equation_params(request)
    try:
        result = equation_instance.forward_transform(request.n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": float(result)}


# Endpoint for inverse transform
@app.post("/inverse-transform")
async def reverse_transform(request: ReverseTransformRequest) -> Dict[str, float]:
    equation_instance = update_equation_params(request)
    try:
        result = equation_instance.inverse_transform(request.weekly_mileage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": float(result)}


# Endpoint for rate of change calculation
@app.post("/rate-of-change")
async def rate_of_change(request: RateOfChangeRequest) -> Dict[str, float]:
    equation_instance = update_equation_params(request)
    try:
        result = equation_instance.rate_of_change_with_respect_to_n(request.n)
    except ValueError:
        return {"result": float("nan")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"result": float(result)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runna Weekly Mileage Model API")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port number (default: 8000)"
    )
    args = parser.parse_args()

    uvicorn.run(
        "weekly_mileage_modelling.api.run:app",
        host="0.0.0.0",
        port=args.port,
        log_level="debug",
        reload=True,
    )
