import pytest
import json
import os
import httpx
from unittest.mock import patch, MagicMock
from library import Book, Library

# Testten önce ve sonra çalışacak fixture'lar
@pytest.fixture
def clean_json_file():
    """Her testten önce ve sonra library.json dosyasını temizler."""
    file_name = "library.json"
    if os.path.exists(file_name):
        os.remove(file_name)
    yield
    if os.path.exists(file_name):
        os.remove(file_name)

@pytest.fixture
def library(clean_json_file):
    """Testler için yeni bir Library nesnesi oluşturur."""
    return Library()

# --- Book Sınıfı için Unit Testler ---

def test_book_creation():
    """Book sınıfının doğru oluşturulduğunu test eder."""
    book = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
    assert book.title == "The Hitchhiker's Guide to the Galaxy"
    assert book.author == "Douglas Adams"
    assert book.isbn == "978-0345391803"
    assert not book.is_borrowed
    assert str(book) == "The Hitchhiker's Guide to the Galaxy by Douglas Adams (ISBN: 978-0345391803)"

def test_borrow_book_success():
    """Kitap ödünç alma işlevini test eder."""
    book = Book("Title", "Author", "123")
    assert book.borrow_book() is True
    assert book.is_borrowed is True

def test_borrow_book_already_borrowed():
    """Ödünç alınmış bir kitabı tekrar alma durumunu test eder."""
    book = Book("Title", "Author", "123")
    book.is_borrowed = True
    assert book.borrow_book() is False
    assert book.is_borrowed is True

def test_return_book_success():
    """Kitap iade etme işlevini test eder."""
    book = Book("Title", "Author", "123")
    book.is_borrowed = True
    assert book.return_book() is True
    assert book.is_borrowed is False

def test_return_book_not_borrowed():
    """Ödünç alınmamış bir kitabı iade etme durumunu test eder."""
    book = Book("Title", "Author", "123")
    assert book.return_book() is False
    assert book.is_borrowed is False

# --- Library Sınıfı için Unit Testler ---

def test_add_book_success(library):
    """Kütüphaneye başarılı kitap ekleme durumunu test eder."""
    book = Book("The Hobbit", "J.R.R. Tolkien", "978-0618053267")
    assert library.add_book(book) is True
    assert len(library.books) == 1

def test_add_book_duplicate(library):
    """Aynı ISBN'e sahip kitabı tekrar ekleme durumunu test eder."""
    book1 = Book("The Hobbit", "J.R.R. Tolkien", "978-0618053267")
    book2 = Book("The Hobbit", "J.R.R. Tolkien", "978-0618053267")
    library.add_book(book1)
    assert library.add_book(book2) is False
    assert len(library.books) == 1

def test_remove_book_success(library):
    """Kütüphaneden başarılı kitap silme durumunu test eder."""
    book = Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618053267")
    library.add_book(book)
    assert library.remove_book("978-0618053267") is True
    assert len(library.books) == 0

def test_remove_nonexistent_book(library):
    """Var olmayan bir kitabı silme durumunu test eder."""
    assert library.remove_book("non-existent-isbn") is False
    assert len(library.books) == 0

def test_load_books_success(library, clean_json_file):
    """Dosyadan kitap yükleme işlevini test eder."""
    book_data = [
        {"title": "Test Title", "author": "Test Author", "isbn": "12345"},
    ]
    with open("library.json", "w") as f:
        json.dump(book_data, f)
    
    library.load_books()
    assert len(library.books) == 1
    assert library.books[0].title == "Test Title"

def test_find_existing_book(library):
    """Mevcut bir kitabı bulma durumunu test eder."""
    book = Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618053267")
    library.add_book(book)
    found_book = library.find_book("978-0618053267")
    assert found_book is not None
    assert found_book.title == "The Lord of the Rings"

def test_find_nonexistent_book(library):
    """Var olmayan bir kitabı bulma durumunu test eder."""
    assert library.find_book("non-existent-isbn") is None

# --- API Entegrasyonu Testleri (Güncellendi) ---

@patch('httpx.Client.get')
def test_get_book_from_api_success(mock_get, library):
    """API'den kitap bulma işlevinin başarılı durumunu test eder."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ISBN:978-0618053267": {
            "title": "The Lord of the Rings",
            "authors": [
                {"name": "J.R.R. Tolkien"}
            ]
        }
    }
    mock_get.return_value = mock_response

    book = library.get_book_from_api("978-0618053267")
    assert book is not None
    assert book.title == "The Lord of the Rings"
    assert book.author == "J.R.R. Tolkien"
    assert book.isbn == "978-0618053267"

@patch('httpx.Client.get')
def test_get_book_from_api_not_found(mock_get, library):
    """API'de kitap bulunamadığı durumu test eder."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    book = library.get_book_from_api("non-existent-isbn")
    assert book is None

@patch('httpx.Client.get')
def test_get_book_from_api_http_error(mock_get, library):
    """API isteği sırasında HTTP hatası oluşması durumunu test eder."""
    mock_get.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=httpx.Request("GET", "http://example.com"), response=httpx.Response(400)
    )

    book = library.get_book_from_api("978-1234567890")
    assert book is None
