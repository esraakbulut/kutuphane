# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from library import Library  # library.py'den Library sınıfını içe aktar

# Pydantic ile veri modelini tanımla
class Book(BaseModel):
    title: str
    author: str
    isbn: str

# FastAPI uygulamasını başlat
app = FastAPI()
library = Library()  # library.py'deki Library sınıfından bir örnek oluştur

@app.get("/books", response_model=list[Book])
def get_all_books():
    """Kütüphanedeki tüm kitapları listeler."""
    return library.books

@app.get("/books/{isbn}", response_model=Optional[Book])
def get_book(isbn: str):
    """Belirli bir ISBN'e sahip kitabı getirir."""
    book = library.find_book(isbn)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kitap bulunamadı")
    return book

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_new_book(book: Book):
    """Kütüphaneye yeni bir kitap ekler."""
    # library.py'deki add_book metodunun başarılı olup olmadığını kontrol et
    if library.add_book(book):
        return {"message": "Kitap başarıyla eklendi."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu ISBN'e sahip kitap zaten mevcut.")

@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(isbn: str):
    """Belirli bir ISBN'e sahip kitabı siler."""
    # library.py'deki remove_book metodunun başarılı olup olmadığını kontrol et
    if not library.remove_book(isbn):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kitap bulunamadı.")
    return None