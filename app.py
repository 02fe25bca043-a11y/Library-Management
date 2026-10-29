
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample library records
books = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "John Smith",
        "available": True
    },
    {
        "id": 2,
        "title": "Introduction to Databases",
        "author": "Mary Jones",
        "available": True
    },
    {
        "id": 3,
        "title": "Computer Networks",
        "author": "David Lee",
        "available": True
    }
]

next_id = 4


@app.route("/", methods=["GET", "POST"])
def home():
    global next_id

    message = ""
    search = ""

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            title = request.form.get("title", "").strip()
            author = request.form.get("author", "").strip()

            if title and author:
                books.append({
                    "id": next_id,
                    "title": title,
                    "author": author,
                    "available": True
                })
                next_id += 1
                message = "Book added successfully."
            else:
                message = "Enter both title and author."

        elif action == "issue":
            book_id = request.form.get("book_id", type=int)
            book = next(
                (b for b in books if b["id"] == book_id),
                None
            )

            if book and book["available"]:
                book["available"] = False
                message = "Book issued successfully."
            else:
                message = "Book unavailable or not found."

        elif action == "return":
            book_id = request.form.get("book_id", type=int)
            book = next(
                (b for b in books if b["id"] == book_id),
                None
            )

            if book and not book["available"]:
                book["available"] = True
                message = "Book returned successfully."
            else:
                message = "Book not issued or not found."

        elif action == "search":
            search = request.form.get("search", "").strip()

    if request.method == "GET":
        search = request.args.get("search", "").strip()

    filtered_books = [
        book for book in books
        if search.lower() in book["title"].lower()
        or search.lower() in book["author"].lower()
    ]

    return render_template(
        "index.html",
        books=filtered_books,
        message=message,
        search=search
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
