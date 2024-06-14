import httpx

base_url = "http://localhost:8000"


# Example forward-transform request
async def test_forward_transform():
    endpoint = "/forward-transform"
    n_value = 10
    url = base_url + endpoint
    payload = {"n": n_value, "a": 0.5, "b": 0.4}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Forward Transform Response: {response.status_code}")
        if response.status_code == 200:
            print(f"Result: {response.json()}")


# Example inverse-transform request
async def test_reverse_transform():
    endpoint = "/inverse-transform"
    weekly_mileage_value = 25
    url = base_url + endpoint
    payload = {"weekly_mileage": weekly_mileage_value, "a": 0.7}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Reverse Transform Response: {response.status_code}")
        if response.status_code == 200:
            print(f"Result: {response.json()}")


# Example rate-of-change request
async def test_rate_of_change():
    endpoint = "/rate-of-change"

    url = base_url + endpoint
    # self.starting_mileage + self.a * self.n / self.b <= self.target_mileage
    payload = {
        "target_mileage": 10 + 0.5 * 10 / 1,
        "n": 10,
        "a": 0.5,
        "b": 1,
        "starting_mileage": 10,
        "equation_choice": "equation2",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Rate of Change Response: {response.status_code}")
        if response.status_code == 200:
            print(f"Result: {response.json()}")
            print(
                "This is expected, as it is the case for eq2 where the derivative is undefined"
            )


async def main():
    await test_forward_transform()
    await test_reverse_transform()
    await test_rate_of_change()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
