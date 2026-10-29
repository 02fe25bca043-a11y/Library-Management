
import pytest
import app as library


@pytest.fixture
def client():
    library.books.clear()
    library.books.extend([
        {
            "id": 1,
            "title": "Python Programming",
            "author": "John Smith",
            "available": True
        }
    ])
    library.next_id = 2

    library.app.config["TESTING"] = True

    with library.app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Python Programming" in response.data


def test_add_book(client):
    response = client.post("/", data={
        "action": "add",
        "title": "Operating Systems",
        "author": "Jane Doe"
    })
    assert response.status_code == 200
    assert b"Operating Systems" in response.data


def test_issue_book(client):
    client.post("/", data={
        "action": "issue",
        "book_id": "1"
    })
    assert library.books[0]["available"] is False


def test_return_book(client):
    library.books[0]["available"] = False

    client.post("/", data={
        "action": "return",
        "book_id": "1"
    })
    assert library.books[0]["available"] is True
