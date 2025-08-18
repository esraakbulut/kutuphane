# 📚 Python 202 Bootcamp Projesi - Kütüphane Yönetim Sistemi  

## 🔎 Genel Bakış  
Bu proje, **Global AI Hub Python 202 Bootcamp** kapsamında geliştirilmiştir.  
Amaç; Python’da **OOP**, **harici API kullanımı** ve **FastAPI ile kendi API’nizi geliştirme** becerilerini birleştirmektir.  

Proje 3 aşamadan oluşmaktadır:  
1. **OOP ile Konsol Uygulaması** → Kitap ekleme, silme, arama ve listeleme.  
2. **Harici API Entegrasyonu** → Open Library API ile ISBN üzerinden kitap bilgisi çekme.  
3. **FastAPI ile Kendi API’niz** → Kütüphaneyi web servisi olarak sunma.  

---

## ⚙️ Kurulum  

### 1. Repoyu Klonlayın  
```bash
git clone https://github.com/esraakbulut/kutuphane.git
cd kutuphane
```

### 2. Sanal Ortam Oluşturun (opsiyonel fakat önerilir)  
```bash
python -m venv venv
source venv/bin/activate   # MacOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Bağımlılıkları Kurun  
```bash
pip install -r requirements.txt
```

---

## 🚀 Kullanım  

### 🔹 Aşama 1 ve 2 – Konsol Uygulaması  
```bash
python main.py
```
📌 Menü:  
1. Kitap Ekle  
2. Kitap Sil  
3. Kitapları Listele  
4. Kitap Ara  
5. Çıkış  

- ISBN girildiğinde, kitap bilgileri **Open Library API**’den otomatik çekilir.  
- Veriler `library.json` dosyasında kalıcı olarak saklanır.  

### 🔹 Aşama 3 – FastAPI Sunucusu  
```bash
uvicorn api:app --reload
```

Ardından tarayıcıdan:  
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → Otomatik API dokümantasyonu  

---

## 📡 API Endpointleri  

| Metod | Endpoint        | Açıklama |
|-------|----------------|----------|
| **GET**    | `/books`           | Kütüphanedeki tüm kitapları listeler |
| **POST**   | `/books`           | Body: `{"isbn": "978-0451524935"}` → Kitabı ekler |
| **DELETE** | `/books/{isbn}`   | ISBN ile kitap siler |

Örnek **POST** isteği:  
```json
{
  "isbn": "978-0451524935"
}
```

---

## ✅ Testler  
Tüm aşamalar için **pytest** test dosyaları yazılmıştır. Çalıştırmak için:  
```bash
pytest
```

---

## 💡 İleri Seviye Geliştirme Fikirleri  
- JSON yerine **SQLite veritabanı** kullanma.  
- **PUT** metodu ile kitap güncelleme özelliği ekleme.  
- API’yi kullanan basit bir **HTML/JS arayüzü** geliştirme.  
- **Docker** ile containerize etme.  
