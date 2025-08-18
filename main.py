from library import Library, Book

def main():
    library = Library()

    while True:
        print("\n### Kütüphane Yönetim Sistemi ###")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == '1':
            title = input("Kitap başlığı: ")
            author = input("Yazar adı: ")
            isbn = input("ISBN: ")
            new_book = Book(title, author, isbn)
            library.add_book(new_book)
        elif choice == '2':
            isbn = input("Silinecek kitabın ISBN'i: ")
            library.remove_book(isbn)
        elif choice == '3':
            library.list_books()
        elif choice == '4':
            isbn = input("Aranacak kitabın ISBN'i: ")
            found_book = library.find_book(isbn)
            if found_book:
                print("Kitap bulundu:", found_book)
            else:
                print("Kitap bulunamadı.")
        elif choice == '5':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()