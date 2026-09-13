#Book - title (str), isbn (int), is_checked_out ()DONE
#Member - borrow_book, return_book(book) -> functions DONE
#BookUnavailableError -> Custom Exception Handler
 #condition: cannot borrow unavailbale book, message + book title DONE

#Task:
#1. add __str__ on Book, shows title and availability DONE

#Results:
#1. successful borrow (DONE)
#2. successful return (DONE)
#3. failed borrow attempt on checked out book (DONE)

class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.is_checked_out = False

    def __str__(self):
        status = "checked out" if self.is_checked_out else "available"
        return f"{self.title} ({status})"

class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book: Book):
        if book.is_checked_out:
            raise BookUnavailableError(book.title)
        book.is_checked_out = True
        self.borrowed_books.append(book)

    def return_book(self, book: Book):
        if book in self.borrowed_books:
            book.is_checked_out = False
            self.borrowed_books.remove(book)

class BookUnavailableError(Exception):
    def __init__(self, title):
        super().__init__(f"{title} is checked out and unavailable.")
        self.title = title

if __name__ == "__main__":
    hobbit = Book("Hobbit", "12345")
    kendra = Member("Kendra")
    gwen = Member("Gwen")

    kendra.borrow_book(hobbit)
    print(hobbit)

    kendra.return_book(hobbit)
    print(hobbit)

    kendra.borrow_book(hobbit)
    try:
        gwen.borrow_book(hobbit)
    except BookUnavailableError as e:
        print(f"Borrow failed: {e}")



