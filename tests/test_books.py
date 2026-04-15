from fastapi import status

# 【测试点 1】: Happy Path (正常情况) - 查询空数据库时返回空列表
def test_list_books_empty(client):
    response = client.get("/api/books")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

# 【测试点 2】: Sad Path (异常情况) - 未带 API Key 尝试创建图书，应被拦截打回 403
def test_create_book_unauthorized(client):
    payload = {"title": "Hack_Test", "ratings_count": 0}
    response = client.post("/api/books", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

# 【测试点 3】: Happy Path (正常情况) - 携带正确 API Key 成功建书
def test_create_book_success(client, auth_headers):
    payload = {
        "title": "pytest从入门到精通",
        "description": "一本自动化测试神书",
        "authors": "TDD Master",
        "published_date": "2023-01-01",
        "ratings_count": 0
    }
    response = client.post("/api/books", json=payload, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "pytest从入门到精通"
    assert "id" in data

# 【测试点 4】: Sad Path (异常情况) - 查询一本根本不存在的书，确认是否抛出规范的 404
def test_get_book_not_found(client):
    response = client.get("/api/books/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"success": False, "error": "Book not found"}
