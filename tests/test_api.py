from weekly_mileage_modelling.api.run import test_client


# test an undefined endpoint to ensure it 404s
def test_read_main():
    response = test_client.get("/bad")
    assert response.status_code == 404


good_request_data = {
    "n": 5,
    "starting_mileage": 10,
    "target_mileage": 50,
    "a": 0.5,
    "b": 3,
}


def test_forward_transform():

    response = test_client.post("/forward-transform", json=good_request_data)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data


# response is imaginary, so is unprocessible.
def test_inverse_transform():
    response = test_client.post("/inverse-transform", json=good_request_data)
    assert response.status_code == 422


def test_rate_of_change():
    response = test_client.post("/rate-of-change", json=good_request_data)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data


def test_inverse_transform_invalid_weekly_mileage():
    request_data = {
        "weekly_mileage": -10,
        "starting_mileage": 10,
        "target_mileage": 50,
        "a": 0.5,
        "b": 3,
    }
    response = test_client.post("/inverse-transform", json=request_data)
    assert response.status_code == 500
    data = response.json()

    assert "detail" in data


def test_inverse_transform_valid():
    request_data = {
        "weekly_mileage": 20,
        "starting_mileage": 10,
        "target_mileage": 50,
        "a": 0.5,
        "b": 3,
    }
    response = test_client.post("/inverse-transform", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
