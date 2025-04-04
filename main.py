import sqlite3


def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readers (
            reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            book_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE SET NULL  -- Добавлена связь с книгами
        )
    """)

    conn.commit()
    conn.close()




def add_book(title, author, year):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()


def add_reader(name, phone):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()



def give_book(reader_id, book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()


    cursor.execute("SELECT 1 FROM readers WHERE reader_id = ?", (reader_id,))
    reader_exists = cursor.fetchone()
    if not reader_exists:
        print("Ошибка: Читатель с ID", reader_id, "не найден.")
        conn.close()
        return

    cursor.execute("SELECT 1 FROM books WHERE book_id = ?", (book_id,))
    book_exists = cursor.fetchone()
    if not book_exists:
        print("Ошибка: Книга с ID", book_id, "не найдена.")
        conn.close()
        return

    cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    if book[0] == 0:
        print("Ошибка: Книга с ID", book_id, "уже выдана.")
        conn.close()
        return

    cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = ? WHERE reader_id = ?", (book_id, reader_id))

    conn.commit()
    conn.close()
    print("Книга с ID", book_id, "выдана читателю с ID", reader_id)

def return_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()


    cursor.execute("SELECT 1 FROM books WHERE book_id = ?", (book_id,))
    book_exists = cursor.fetchone()
    if not book_exists:
        print("Ошибка: Книга с ID", book_id, "не найдена.")
        conn.close()
        return


    cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    if book[0] == 1:
        print("Ошибка: Книга с ID", book_id, "уже находится в библиотеке.")
        conn.close()
        return


    cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE readers SET book_id = NULL WHERE book_id = ?", (book_id,))

    conn.commit()
    conn.close()
    print("Книга с ID", book_id, "возвращена в библиотеку")



def get_available_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT book_id, title, author FROM books WHERE available = 1")
    books = cursor.fetchall()
    conn.close()
    return books


def get_reader_books(reader_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT books.title, books.author
        FROM readers
        JOIN books ON readers.book_id = books.book_id
        WHERE readers.reader_id = ?
    """, (reader_id,))
    books = cursor.fetchall()
    conn.close()
    return books


def search_books(keyword):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT book_id, title, author
        FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    conn.close()
    return books



def print_books(books):
    if books:
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
    else:
        print("Нет доступных книг.")



create_database()


add_book("Мастер и Маргарита", "Михаил Булгаков", 1967)
add_book("1984", "Джордж Оруэлл", 1949)
add_book("Гарри Поттер и философский камень", "Джоан Роулинг", 1997)


add_reader("Иван Петров", "123-45-67")
add_reader("Мария Сидорова", "987-65-43")

give_book(1, 1)

print("\nДоступные книги:")
available_books = get_available_books()
print_books(available_books)


return_book(1)


print("\nДоступные книги после возврата:")
available_books = get_available_books()
print_books(available_books)

