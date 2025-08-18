import pytest
from fastapi.testclient import TestClient
from api import app, library
from library import Book
import os

# Testten önce ve sonra çalışacak fixture'lar
@pytest.fixture
def client():
    """FastAPI TestClient nesnesi oluşturur."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_up_library_data():
    """Her testten önce ve sonra kütüphane verilerini sıfırlar."""
    library.books = []
    if os.path.exists("library.json"):
        os.remove("library.json")
    yield  # Testin çalışmasını bekler
    library.books = []
    if os.path.exists("library.json"):
        os.remove("library.json")

# --- FastAPI Endpoint Testleri ---

def test_get_all_books(client):
    """GET /books endpoint'ini test eder."""
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book_success(client):
    """POST /books endpoint'ini başarılı bir ekleme için test eder."""
    new_book = {
        "title": "The Martian",
        "author": "Andy Weir",
        "isbn": "978-0553418026"
    }
    response = client.post("/books", json=new_book)
    assert response.status_code == 201
    assert "message" in response.json()

def test_add_existing_book_failure(client):
    """Mevcut bir kitabı ekleme durumunu test eder."""
    existing_book = {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "978-0441172719"
    }
    client.post("/books", json=existing_book)
    response = client.post("/books", json=existing_book)
    assert response.status_code == 409

def test_get_book_by_isbn_success(client):
    """GET /books/{isbn} endpoint'ini başarılı bir arama için test eder."""
    book_to_add = {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "isbn": "978-0553293357"
    }
    client.post("/books", json=book_to_add)
    response = client.get("/books/978-0553293357")
    assert response.status_code == 200
    assert response.json()["title"] == "Foundation"

def test_get_book_by_isbn_not_found(client):
    """Var olmayan bir kitabı arama durumunu test eder."""
    response = client.get("/books/nonexistent-isbn")
    assert response.status_code == 404
    assert "Kitap bulunamadı" in response.json()["detail"]

def test_delete_book_success(client):
    """DELETE /books/{isbn} endpoint'ini başarılı bir silme için test eder."""
    book_to_delete = {
        "title": "The Three-Body Problem",
        "author": "Liu Cixin",
        "isbn": "978-0765382890"
    }
    client.post("/books", json=book_to_delete)
    response = client.delete("/books/978-0765382890")
    assert response.status_code == 204

def test_delete_book_not_found(client):
    """Var olmayan bir kitabı silme durumunu test eder."""
    response = client.delete("/books/nonexistent-isbn")
    assert response.status_code == 404
    assert "Kitap bulunamadı" in response.json()["detail"]