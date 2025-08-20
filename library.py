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
            books_data = [b.__dict__ for b in self.books]
            json.dump(books_data, f, indent=4)

    def add_book(self, book):
        if not self.find_book(book.isbn):
            self.books.append(book)
            self.save_books()
            return True
        return False

    def remove_book(self, isbn):
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"'{book.title}' kütüphaneden silindi.")
            return True
        print("Kitap bulunamadı.")
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
        
    def get_book_from_api(self, isbn):
        """
        Open Library API'den ISBN ile kitap bilgisi çeker.
        """
        base_url = "https://openlibrary.org/api/books"
        params = {
            "bibkeys": f"ISBN:{isbn}",
            "jscmd": "data",
            "format": "json"
        }
        try:
            with httpx.Client() as client:
                response = client.get(base_url, params=params)
                response.raise_for_status() # HTTP hatalarını kontrol et
                data = response.json()
                
                book_data = data.get(f"ISBN:{isbn}")
                if book_data:
                    title = book_data.get("title")
                    authors = book_data.get("authors", [])
                    author_name = authors[0].get("name") if authors else "Bilinmiyor"
                    
                    if title and author_name:
                        print(f"API'den kitap bilgisi çekildi: {title} by {author_name}")
                        return Book(title, author_name, isbn)
                    else:
                        print("API'den gerekli bilgiler (başlık veya yazar) çekilemedi.")
                        return None
                else:
                    print("API'de bu ISBN'e ait kitap bulunamadı.")
                    return None
        except httpx.HTTPError as e:
            print(f"API isteği sırasında bir hata oluştu: {e}")
            return None
