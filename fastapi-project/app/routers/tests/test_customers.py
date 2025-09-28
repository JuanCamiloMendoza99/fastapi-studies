from fastapi import status


def test_create_customer(client):
    customer_test = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "description": "A regular customer",
    }

    response = client.post(
        "/customers/",
        json=customer_test,
    )
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client):
    customer_test = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "description": "A regular customer",
    }

    response = client.post(
        "/customers/",
        json=customer_test,
    )

    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json().get("id")

    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json().get("name") == customer_test.get("name")
    assert response_read.json().get("email") == customer_test.get("email")
    assert response_read.json().get("age") == customer_test.get("age")
    assert response_read.json().get("description") == customer_test.get("description")
