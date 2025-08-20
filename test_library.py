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

def test_book_borrow_and_return():
    """Kitap ödünç alma ve geri verme işlevlerini test eder."""
    book = Book("Test Book", "Test Author", "12345")
    assert book.borrow_book()
    assert book.is_borrowed
    assert not book.borrow_book()  # Zaten ödünç alınmışsa false dönmeli
    assert book.return_book()
    assert not book.is_borrowed
    assert not book.return_book()  # Zaten geri verilmişse false dönmeli

# --- Library Sınıfı için Unit Testler ---

def test_add_book(library):
    """Kütüphaneye kitap ekleme işlevini test eder."""
    book = Book("Dune", "Frank Herbert", "978-0441172719")
    assert library.add_book(book)
    assert len(library.books) == 1
    assert library.books[0].isbn == "978-0441172719"

def test_add_existing_book(library):
    """Zaten var olan bir kitabı ekleme durumunu test eder."""
    book1 = Book("Dune", "Frank Herbert", "978-0441172719")
    book2 = Book("Dune", "Frank Herbert", "978-0441172719")
    library.add_book(book1)
    assert not library.add_book(book2)
    assert len(library.books) == 1

def test_remove_book(library):
    """Kütüphaneden kitap silme işlevini test eder."""
    book = Book("1984", "George Orwell", "978-0451524935")
    library.add_book(book)
    assert library.remove_book("978-0451524935")
    assert len(library.books) == 0

def test_remove_nonexistent_book(library):
    """Var olmayan bir kitabı silme durumunu test eder."""
    assert not library.remove_book("non-existent-isbn")

def test_find_book(library):
    """ISBN ile kitap bulma işlevini test eder."""
    book = Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618053267")
    library.add_book(book)
    found_book = library.find_book("978-0618053267")
    assert found_book is not None
    assert found_book.title == "The Lord of the Rings"

def test_find_nonexistent_book(library):
    """Var olmayan bir kitabı bulma durumunu test eder."""
    assert library.find_book("non-existent-isbn") is None

# --- API Entegrasyonu Testi ---

@patch('httpx.Client.get')
def test_search_book_api_success(mock_get, library):
    """API'den kitap arama işlevinin başarılı durumunu test eder."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "docs": [
            {
                "title": "The Hobbit",
                "author_name": ["J.R.R. Tolkien"],
                "isbn": ["978-0618053267"]
            }
        ]
    }
    mock_get.return_value = mock_response
    
    books = library.search_book_api("The Hobbit")
    assert len(books) == 1
    assert books[0].title == "The Hobbit"
    assert books[0].author == "J.R.R. Tolkien"
    assert books[0].isbn == "978-0618053267"

@patch('httpx.Client.get')
def test_search_book_api_not_found(mock_get, library):
    """API'de kitap bulunamadığı durumu test eder."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"docs": []}
    mock_get.return_value = mock_response
    
    books = library.search_book_api("Non-Existent Book")
    assert len(books) == 0