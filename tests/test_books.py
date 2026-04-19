from fastapi import status

# --- Helpers -----------------------------------------------------------------


def _book_payload(
    title: str,
    *,
    description: str | None = None,
    categories: str | None = None,
    ratings_count: int = 0,
) -> dict:
    return {
        "title": title,
        "description": description,
        "authors": None,
        "publisher": None,
        "published_date": None,
        "categories": categories,
        "ratings_count": ratings_count,
    }


def _create_book(client, auth_headers: dict, **kwargs) -> dict:
    payload = _book_payload(**kwargs)
    r = client.post("/api/books", json=payload, headers=auth_headers)
    assert r.status_code == status.HTTP_201_CREATED, r.text
    return r.json()


# --- GET /api/books ----------------------------------------------------------


def test_list_books_empty(client):
    response = client.get("/api/books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_list_books_pagination_query_category(client, auth_headers):
    _create_book(client, auth_headers, title="Alpha Python Guide", categories="Computers")
    _create_book(client, auth_headers, title="Beta Cooking", categories="Cooking")
    _create_book(client, auth_headers, title="Gamma Python Tips", categories="Computers")

    all_items = client.get("/api/books?limit=100").json()
    assert len(all_items) == 3

    page = client.get("/api/books?skip=1&limit=1").json()
    assert len(page) == 1

    python_only = client.get("/api/books?query=Python").json()
    assert len(python_only) == 2
    assert all("Python" in b["title"] for b in python_only)

    computers = client.get("/api/books?category=Computers").json()
    assert len(computers) == 2


def test_list_books_invalid_skip_unprocessable(client):
    r = client.get("/api/books?skip=-1")
    assert r.status_code == 422


def test_list_books_invalid_limit_unprocessable(client):
    r = client.get("/api/books?limit=0")
    assert r.status_code == 422
    r = client.get("/api/books?limit=101")
    assert r.status_code == 422


# --- GET /api/books/stats ----------------------------------------------------


def test_get_books_stats_empty(client):
    r = client.get("/api/books/stats")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["total_books"] == 0
    assert data["average_ratings_count"] == 0


def test_get_books_stats_with_data(client, auth_headers):
    _create_book(client, auth_headers, title="S1", ratings_count=10)
    _create_book(client, auth_headers, title="S2", ratings_count=20)
    r = client.get("/api/books/stats")
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert data["total_books"] == 2
    assert data["average_ratings_count"] == 15.0


# --- GET /api/books/{book_id} ------------------------------------------------


def test_get_book_success(client, auth_headers):
    created = _create_book(client, auth_headers, title="Single Book")
    r = client.get(f"/api/books/{created['id']}")
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["title"] == "Single Book"


def test_get_book_not_found(client):
    response = client.get("/api/books/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"success": False, "error": "Book not found"}


def test_get_book_invalid_id_type_unprocessable(client):
    r = client.get("/api/books/not-an-integer")
    assert r.status_code == 422


# --- POST /api/books ---------------------------------------------------------


def test_create_book_success(client, auth_headers):
    payload = {
        "title": "pytest from zero to hero",
        "description": "A great book regarding automated testing",
        "authors": "TDD Master",
        "published_date": "2023-01-01",
        "ratings_count": 0,
    }
    response = client.post("/api/books", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "pytest from zero to hero"
    assert "id" in data


def test_create_book_unauthorized(client):
    payload = {"title": "Hack_Test", "ratings_count": 0}
    response = client.post("/api/books", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_book_invalid_api_key(client):
    payload = _book_payload("X")
    r = client.post("/api/books", json=payload, headers={"X-API-Key": "wrong-key"})
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_create_book_validation_empty_title_unprocessable(client, auth_headers):
    r = client.post("/api/books", json={"title": "", "ratings_count": 0}, headers=auth_headers)
    assert r.status_code == 422


def test_create_book_validation_negative_ratings_unprocessable(client, auth_headers):
    r = client.post(
        "/api/books",
        json={"title": "Bad ratings", "ratings_count": -1},
        headers=auth_headers,
    )
    assert r.status_code == 422


# --- PUT /api/books/{book_id} ------------------------------------------------


def test_update_book_success(client, auth_headers):
    created = _create_book(client, auth_headers, title="Old Title")
    r = client.put(
        f"/api/books/{created['id']}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["title"] == "New Title"


def test_update_book_not_found(client, auth_headers):
    r = client.put("/api/books/99999", json={"title": "Nope"}, headers=auth_headers)
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json()["success"] is False


def test_update_book_unauthorized(client):
    r = client.put("/api/books/1", json={"title": "Nope"})
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_update_book_validation_empty_title_unprocessable(client, auth_headers):
    created = _create_book(client, auth_headers, title="Valid")
    r = client.put(f"/api/books/{created['id']}", json={"title": ""}, headers=auth_headers)
    assert r.status_code == 422


# --- DELETE /api/books/{book_id} ---------------------------------------------


def test_delete_book_success(client, auth_headers):
    created = _create_book(client, auth_headers, title="To Delete")
    book_id = created["id"]
    r = client.delete(f"/api/books/{book_id}", headers=auth_headers)
    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/api/books/{book_id}").status_code == status.HTTP_404_NOT_FOUND


def test_delete_book_not_found(client, auth_headers):
    r = client.delete("/api/books/99999", headers=auth_headers)
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_delete_book_unauthorized(client):
    r = client.delete("/api/books/1")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_delete_book_invalid_id_type_unprocessable(client, auth_headers):
    r = client.delete("/api/books/abc", headers=auth_headers)
    assert r.status_code == 422
