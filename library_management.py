import sqlite3
from typing import List, Optional


class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(self, title: str, author: str, year: int, book_id: Optional[int] = None, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status


class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self, db_name: str = "library.db"):
        self.conn = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        """Создает таблицу для хранения книг, если её нет."""
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            status TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        query = "INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (title, author, year, "в наличии"))
        self.conn.commit()
        print("Книга успешно добавлена!")

    def remove_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки по её id."""
        query = "DELETE FROM books WHERE id = ?"
        cursor = self.conn.execute(query, (book_id,))
        self.conn.commit()
        if cursor.rowcount:
            print("Книга успешно удалена!")
        else:
            print("Книга с таким ID не найдена!")

    def search_books(self, keyword: str) -> List[Book]:
        """Ищет книги по ключевому слову (название, автор или год)."""
        query = """
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR year LIKE ?
        """
        cursor = self.conn.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        return [Book(*row) for row in cursor.fetchall()]

    def list_books(self) -> List[Book]:
        """Возвращает список всех книг в библиотеке."""
        query = "SELECT * FROM books"
        cursor = self.conn.execute(query)
        return [Book(*row) for row in cursor.fetchall()]

    def update_status(self, book_id: int, new_status: str) -> None:
        """Изменяет статус книги."""
        if new_status not in ["в наличии", "выдана"]:
            print("Недопустимый статус!")
            return
        query = "UPDATE books SET status = ? WHERE id = ?"
        cursor = self.conn.execute(query, (new_status, book_id))
        self.conn.commit()
        if cursor.rowcount:
            print("Статус книги успешно обновлен!")
        else:
            print("Книга с таким ID не найдена!")

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска: ")
            results = library.search_books(keyword)
            if results:
                for book in results:
                    print(f"{book.id}: {book.title} - {book.author} ({book.year}) [{book.status}]")
            else:
                print("Книги не найдены!")

        elif choice == "4":
            books = library.list_books()
            if books:
                for book in books:
                    print(f"{book.id}: {book.title} - {book.author} ({book.year}) [{book.status}]")
            else:
                print("Библиотека пуста!")

        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)

        elif choice == "6":
            library.close()
            print("Выход из программы...")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
