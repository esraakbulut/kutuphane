import json
import httpx # 'httpx' kütüphanesi kullanılacak

# Aşama 1'deki Book sınıfı buraya eklenecek
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def borrow_book(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False

class Library:
    def __init__(self, file_name="library.json"):
        self.file_name = file_name
        self.books = []
        self.load_books()

    def load_books(self):
        try:
            with open(self.file_name, "r") as f:
                books_data = json.load(f)
                self.books = [Book(b['title'], b['author'], b['isbn']) for b in books_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def save_books(self):
        with open(self.file_name, "w") as f:
            books_data = [{"title": b.title, "author": b.author, "isbn": b.isbn} for b in self.books]
            json.dump(books_data, f, indent=4)

    def add_book(self, book):
        if not self.find_book(book.isbn):
            self.books.append(book)
            self.save_books()
            print(f"'{book.title}' kütüphaneye eklendi.")
            return True
        print(f"'{book.title}' zaten kütüphanede mevcut.")
        return False

    def remove_book(self, isbn):
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"ISBN {isbn} numaralı kitap kütüphaneden silindi.")
            return True
        print(f"ISBN {isbn} numaralı kitap bulunamadı.")
        return False

    def list_books(self):
        if not self.books:
            print("Kütüphane boş.")
            return
        for book in self.books:
            print(book)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_book_api(self, query):
        base_url = "https://openlibrary.org/search.json"
        params = {"q": query, "limit": 5}
        try:
            with httpx.Client() as client:
                response = client.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'docs' in data and data['docs']:
                    books_found = []
                    for doc in data['docs']:
                        title = doc.get("title")
                        author = doc.get("author_name", ["Bilinmiyor"])[0]
                        isbn = doc.get("isbn", [None])[0]
                        if title and author and isbn:
                            books_found.append(Book(title, author, isbn))
                    return books_found
                else:
                    print("API'de kitap bulunamadı.")
                    return []
        except httpx.HTTPError as e:
            print(f"API isteği sırasında bir hata oluştu: {e}")
            return []

# main.py dosyasını güncelleyin
# 4. seçenek yerine yeni bir 4. seçenek ekleyin: 'API ile Kitap Ara'
# 5. seçenek 'Kitap Ara' ve 6. seçenek 'Çıkış' olsun.