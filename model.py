from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bookstore"]
books = db.books

sample_books = [
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "price": 299,
        "image_url": "https://covers.openlibrary.org/b/id/10504741-L.jpg"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "price": 250,
        "image_url": "https://covers.openlibrary.org/b/id/10512747-L.jpg"
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "price": 350,
        "image_url": "https://covers.openlibrary.org/b/id/11112745-L.jpg"
    }
]

books.insert_many(sample_books)
print("Books inserted!")
