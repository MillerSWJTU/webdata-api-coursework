from fastapi import status


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


def _review_payload(score: float = 4.0, **extra) -> dict:
    base = {
        "score": score,
        "user_id": "u1",
        "profile_name": "Tester",
        "summary": "Nice",
        "review_text": "Body",
        "review_time": "2024-01-01",
    }
    base.update(extra)
    return base


# --- GET /api/books/{book_id}/reviews ---------------------------------------


def test_list_reviews_empty_for_existing_book(client, auth_headers):
    book = _create_book(client, auth_headers, title="No Reviews Yet")
    r = client.get(f"/api/books/{book['id']}/reviews")
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == []


def test_list_reviews_book_not_found(client):
    r = client.get("/api/books/9999/reviews")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json() == {"success": False, "error": "Book not found"}


def test_list_reviews_invalid_book_id_unprocessable(client):
    r = client.get("/api/books/not-int/reviews")
    assert r.status_code == 422


def test_list_reviews_invalid_skip_unprocessable(client, auth_headers):
    book = _create_book(client, auth_headers, title="B")
    r = client.get(f"/api/books/{book['id']}/reviews?skip=-1")
    assert r.status_code == 422


def test_list_reviews_invalid_limit_unprocessable(client, auth_headers):
    book = _create_book(client, auth_headers, title="B2")
    r = client.get(f"/api/books/{book['id']}/reviews?limit=0")
    assert r.status_code == 422


def test_list_reviews_invalid_min_score_unprocessable(client, auth_headers):
    book = _create_book(client, auth_headers, title="B3")
    r = client.get(f"/api/books/{book['id']}/reviews?min_score=6")
    assert r.status_code == 422


def test_list_reviews_pagination_and_min_score(client, auth_headers):
    book = _create_book(client, auth_headers, title="Reviewed Book")
    bid = book["id"]
    for score in (2.0, 4.5, 5.0):
        rr = client.post(
            f"/api/books/{bid}/reviews",
            json=_review_payload(score=score, summary=f"s{score}"),
            headers=auth_headers,
        )
        assert rr.status_code == status.HTTP_201_CREATED, rr.text

    all_rev = client.get(f"/api/books/{bid}/reviews?limit=50").json()
    assert len(all_rev) == 3

    high = client.get(f"/api/books/{bid}/reviews?min_score=4.0").json()
    assert len(high) == 2
    assert all(x["score"] >= 4.0 for x in high)

    page = client.get(f"/api/books/{bid}/reviews?skip=1&limit=1").json()
    assert len(page) == 1


# --- POST /api/books/{book_id}/reviews ---------------------------------------


def test_create_review_success(client, auth_headers):
    book = _create_book(client, auth_headers, title="For Review")
    r = client.post(
        f"/api/books/{book['id']}/reviews",
        json=_review_payload(score=5.0, summary="Excellent"),
        headers=auth_headers,
    )
    assert r.status_code == status.HTTP_201_CREATED
    data = r.json()
    assert data["book_id"] == book["id"]
    assert data["score"] == 5.0
    assert data["summary"] == "Excellent"
    assert "id" in data


def test_create_review_book_not_found(client, auth_headers):
    r = client.post(
        "/api/books/99999/reviews",
        json=_review_payload(),
        headers=auth_headers,
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_create_review_unauthorized(client, auth_headers):
    book = _create_book(client, auth_headers, title="Locked")
    r = client.post(f"/api/books/{book['id']}/reviews", json=_review_payload())
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_create_review_invalid_api_key(client, auth_headers):
    book = _create_book(client, auth_headers, title="K")
    r = client.post(
        f"/api/books/{book['id']}/reviews",
        json=_review_payload(),
        headers={"X-API-Key": "wrong"},
    )
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_create_review_invalid_score_too_high_unprocessable(client, auth_headers):
    book = _create_book(client, auth_headers, title="Hi")
    r = client.post(
        f"/api/books/{book['id']}/reviews",
        json=_review_payload(score=5.01),
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_create_review_invalid_score_negative_unprocessable(client, auth_headers):
    book = _create_book(client, auth_headers, title="Lo")
    r = client.post(
        f"/api/books/{book['id']}/reviews",
        json=_review_payload(score=-0.1),
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_create_review_invalid_book_id_unprocessable(client, auth_headers):
    r = client.post(
        "/api/books/abc/reviews",
        json=_review_payload(),
        headers=auth_headers,
    )
    assert r.status_code == 422
