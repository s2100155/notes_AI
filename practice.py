Set A — Python OOP / Error Handling

A1 (Library Loan Tracker): Custom exceptions — building your own Exception subclass with a useful message.
A2 (Shape Hierarchy): Abstract base classes (abc.ABC) — forcing subclasses to implement shared methods, and trusting polymorphism instead of isinstance checks.
A3 (Retry-Safe API Caller): try/except retry loops — catching a specific exception, retrying, and raising your own error after repeated failure.
A4 (Employee Payroll): Class attributes vs. instance attributes — the trap where one shared value should update everyone at once.
A5 (Logging Decorator): Decorators — wrapping a function to add behavior (logging) without touching its original code, using functools.wraps.

Set B — Data / Pandas / NumPy / Sklearn

B1 (Messy Survey Cleanup): Pandas data cleaning — stripping whitespace, fixing inconsistent case, filling missing values, dropping duplicates.
B2 (Vectorized Grading Curve): NumPy vectorization — applying math to a whole array at once (no loops) using broadcasting and np.clip/np.where.
B3 (Nearest Neighbor by Hand): Cosine similarity — comparing vectors to find the "closest match" using sklearn.
B4 (Spam Filter Confusion Matrix): Classification metrics — confusion matrix, precision, recall, F1, and reasoning about false positives vs. false negatives.
B5 (Token Budget Estimator): Practical estimation function — summing a heuristic count across items and raising a clear error when a limit is exceeded.



#===================================================================================================



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

#=============================================================================================================

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



#=================================================================================

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError(f"radius must be positive, got {radius}")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        if width <= 0:
            raise ValueError(f"width must be positive, got {width}")
        if height <= 0:
            raise ValueError(f"height must be positive, got {height}")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        if side_a <= 0:
            raise ValueError(f"side_a must be positive, got {side_a}")
        if side_b <= 0:
            raise ValueError(f"side_b must be positive, got {side_b}")
        if side_c <= 0:
            raise ValueError(f"side_c must be positive, got {side_c}")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        # Heron's formula
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


def total_area(shapes: list[Shape]) -> float:
    return sum(shape.area() for shape in shapes)


# --- Demo ---

# 1. Attempting to instantiate Shape directly fails
try:
    s = Shape()
except TypeError as e:
    print(f"Can't instantiate Shape directly: {e}")

# 2. Non-positive dimension raises ValueError
try:
    bad_circle = Circle(-5)
except ValueError as e:
    print(f"Validation caught it: {e}")

# 3. Normal usage — mixed shape types
shapes = [
    Circle(3),
    Rectangle(4, 5),
    Triangle(3, 4, 5),
]

for shape in shapes:
    print(f"{type(shape).__name__}: area={shape.area():.2f}, perimeter={shape.perimeter():.2f}")

# 4. total_area works polymorphically across mixed types
print(f"Total area of all shapes: {total_area(shapes):.2f}")



#=======================================================================================================

import random


class AllRetriesFailedError(Exception):
    def __init__(self, attempts):
        super().__init__(f"All {attempts} attempts failed.")
        self.attempts = attempts


def unreliable_call():
    """Simulated flaky function — ~50% chance of ConnectionError."""
    if random.random() < 0.5:
        raise ConnectionError("Simulated network failure")
    return "Success!"


def safe_call(func, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except ConnectionError as e:
            print(f"Attempt {attempt} failed: {e}")
    raise AllRetriesFailedError(max_retries)


# --- Demo ---

# Run it a few times — since it's random, you'll see different outcomes
for trial in range(1, 4):
    print(f"\n--- Trial {trial} ---")
    try:
        result = safe_call(unreliable_call)
        print(f"Result: {result}")
    except AllRetriesFailedError as e:
        print(f"Gave up: {e}")



#====================================================================================================================


class Employee:
    tax_rate = 0.2  # class attribute — shared by ALL instances

    def __init__(self, name, base_salary):
        self.name = name                # instance attribute
        self.base_salary = base_salary  # instance attribute

    def net_pay(self):
        return self.base_salary * (1 - Employee.tax_rate)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["base_salary"])


# --- Demo ---

alice = Employee("Alice", 60000)
bob = Employee.from_dict({"name": "Bob", "base_salary": 75000})

print(f"{alice.name}: net_pay = {alice.net_pay():.2f}")
print(f"{bob.name}: net_pay = {bob.net_pay():.2f}")

# Now change the tax rate ONCE, on the class itself
Employee.tax_rate = 0.25

print("\n--- After changing Employee.tax_rate to 0.25 ---")
print(f"{alice.name}: net_pay = {alice.net_pay():.2f}")
print(f"{bob.name}: net_pay = {bob.net_pay():.2f}")




#====================================================================================================================



import functools
import datetime


def log_grades(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        timestamp = datetime.datetime.now()
        print(f"[{timestamp}] called {func.__name__} with {args} -> {result}")
        return result
    return wrapper


@log_grades
def calculate_grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


# --- Demo ---

grade1 = calculate_grade(95)
grade2 = calculate_grade(72)
grade3 = calculate_grade(50)

print(f"\ncalculate_grade.__name__ = {calculate_grade.__name__}")
print(f"calculate_grade.__doc__  = {calculate_grade.__doc__}")

# Why functools.wraps matters here:
# Without it, wrapper() replaces calculate_grade in the namespace entirely, so
# calculate_grade.__name__ would report "wrapper" instead of "calculate_grade",
# breaking debugging, logging tools, and any code that introspects the function's
# identity (e.g. another decorator stacked on top, or a test that checks __name__).


#=============================================================================================================


import pandas as pd
import numpy as np

# Hardcoded messy survey data — matches the scenario description:
# extra whitespace, mixed-case "Yes"/"yes"/"YES", missing ages, one duplicate row
data = [
    {"name": "Alice", "response": " Yes ", "age": 25},
    {"name": "Bob", "response": "no", "age": 30},
    {"name": "Carol", "response": "YES", "age": None},
    {"name": "Dave", "response": " No ", "age": 40},
    {"name": "Eve", "response": "yes", "age": 22},
    {"name": "Frank", "response": " NO", "age": None},
    {"name": "Grace", "response": "Yes ", "age": 35},
    {"name": "Heidi", "response": "no ", "age": 28},
    {"name": "Alice", "response": " Yes ", "age": 25},  # exact duplicate of row 1
]

df = pd.DataFrame(data)

print("=== BEFORE cleaning ===")
print(df)
print(df.describe())

# 1. Strip whitespace and normalize case on the text column
df["response"] = df["response"].str.strip().str.capitalize()

# 2. Fill missing age values with the column mean
df["age"] = df["age"].fillna(df["age"].mean())

# 3. Remove exact duplicate rows
df = df.drop_duplicates()

print("\n=== AFTER cleaning ===")
print(df)
print(df.describe())


#====================================================================================================================



import numpy as np

scores = np.array([62, 78, 95, 88, 40, 99, 71])

# Method 1: using np.clip
curved_scores = np.clip(scores + 5, a_min=None, a_max=100)

print("Original scores:", scores)
print("Curved scores:  ", curved_scores)

# Why vectorized is faster than a loop for large arrays:
# NumPy operations run as compiled, pre-optimized C code operating on the whole
# array's contiguous memory block at once, instead of Python's interpreter
# looping one element at a time (with all the overhead of type-checking and
# function calls that comes with every single Python-level iteration). The
# larger the array, the more that per-element Python overhead adds up, while
# the vectorized version's per-element cost stays effectively constant.



#===================================================================================================================


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 4 existing customer profiles: [recency (days), frequency (visits/month), monetary ($)]
customers = np.array([
    [10, 5, 200],   # Customer A — recent, frequent, high spend
    [90, 1, 20],    # Customer B — long ago, rare, low spend
    [15, 4, 180],   # Customer C — recent, frequent, high spend (similar to A)
    [60, 2, 50],    # Customer D — moderate recency, low frequency/spend
])
customer_names = ["A", "B", "C", "D"]

# New customer to compare against
new_customer = np.array([[12, 5, 190]])  # note: 2D shape, sklearn expects this

# Compute cosine similarity between new_customer and all 4 existing customers
similarities = cosine_similarity(new_customer, customers)[0]  # [0] unwraps the single row

# Pair each customer name with their similarity score, then sort highest to lowest
results = sorted(zip(customer_names, similarities), key=lambda x: x[1], reverse=True)

print("Similarity scores (highest to lowest):")
for name, score in results:
    print(f"  Customer {name}: {score:.4f}")

best_match = results[0]
print(f"\nClosest match: Customer {best_match[0]} (similarity = {best_match[1]:.4f})")



#=============================================================================================



from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

# 10 test emails — expected (ground truth) vs predicted (what the filter said)
# Includes 2 deliberate mistakes: one false positive, one false negative
expected_labels  = ["spam", "spam", "not_spam", "not_spam", "spam",
                    "not_spam", "spam", "not_spam", "spam", "not_spam"]
predicted_labels = ["spam", "spam", "not_spam", "spam",     "spam",
                    "not_spam", "not_spam", "not_spam", "spam", "not_spam"]
# ^ index 3: expected not_spam, predicted spam  → false positive
# ^ index 6: expected spam, predicted not_spam  → false negative

# Confusion matrix — specify labels order explicitly so rows/cols are predictable
labels = ["spam", "not_spam"]
cm = confusion_matrix(expected_labels, predicted_labels, labels=labels)

print("Confusion Matrix:")
print(f"                 predicted_spam  predicted_not_spam")
print(f"actual_spam           {cm[0][0]:<15} {cm[0][1]}")
print(f"actual_not_spam       {cm[1][0]:<15} {cm[1][1]}")

# Precision, recall, F1 — specifically for the "spam" class
precision = precision_score(expected_labels, predicted_labels, pos_label="spam")
recall = recall_score(expected_labels, predicted_labels, pos_label="spam")
f1 = f1_score(expected_labels, predicted_labels, pos_label="spam")

print(f"\nPrecision (spam): {precision:.2f}")
print(f"Recall (spam):    {recall:.2f}")
print(f"F1 Score (spam):  {f1:.2f}")


#============================================================================================



def estimate_tokens(text: str) -> int:
    """Rough token estimate using the len(text) // 4 heuristic."""
    return len(text) // 4


def check_token_budget(chunks: list[str], max_context: int = 8000, reserved_for_output: int = 1000) -> int:
    available_budget = max_context - reserved_for_output
    total_tokens = sum(estimate_tokens(chunk) for chunk in chunks)

    if total_tokens > available_budget:
        over_by = total_tokens - available_budget
        raise ValueError(
            f"Chunk batch exceeds token budget: {total_tokens} tokens estimated, "
            f"but only {available_budget} available "
            f"(max_context={max_context}, reserved_for_output={reserved_for_output}). "
            f"Over budget by {over_by} tokens."
        )

    print(f"OK: {total_tokens} tokens used out of {available_budget} available "
          f"({available_budget - total_tokens} tokens to spare).")
    return total_tokens


# --- Demo ---

# Case 1: under budget — short chunks
short_chunks = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning models require large amounts of training data.",
    "RAG pipelines combine retrieval with generation for better answers.",
    "Token limits vary between different language models.",
    "Context windows determine how much text a model can process at once.",
]

print("--- Test 1: under budget ---")
check_token_budget(short_chunks)

# Case 2: over budget — deliberately long chunks
long_chunks = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100,
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " * 100,
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris. " * 100,
    "Duis aute irure dolor in reprehenderit in voluptate velit esse. " * 100,
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui. " * 100,
    "Officia deserunt mollit anim id est laborum sed ut perspiciatis. " * 100,
]

print("\n--- Test 2: over budget ---")
try:
    check_token_budget(long_chunks)
except ValueError as e:
    print(f"Budget check failed: {e}")