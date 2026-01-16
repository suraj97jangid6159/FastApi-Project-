def test_duplicate_email(client, token):
    response = client.post(
        "/api/employees/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test", "email": "test@test.com"}
    )
    assert response.status_code == 400
