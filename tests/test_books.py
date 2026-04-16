from fastapi import status

# [Test Point 1] Happy Path - Return empty list when querying empty DB
def test_list_books_empty(client):
    response = client.get("/api/books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

# [Test Point 2] Sad Path - Attempt creation without API Key, should be intercepted with 403
def test_create_book_unauthorized(client):
    payload = {"title": "Hack_Test", "ratings_count": 0}
    response = client.post("/api/books", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

# [Test Point 3] Happy Path - Successfully create book with correct API Key
def test_create_book_success(client, auth_headers):
    payload = {
        "title": "pytest from zero to hero",
        "description": "A great book regarding automated testing",
        "authors": "TDD Master",
        "published_date": "2023-01-01",
        "ratings_count": 0
    }
    response = client.post("/api/books", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "pytest from zero to hero"
    assert "id" in data

# [Test Point 4] Sad Path - Query a non-existent book, verify proper 404 response
def test_get_book_not_found(client):
    response = client.get("/api/books/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"success": False, "error": "Book not found"}
