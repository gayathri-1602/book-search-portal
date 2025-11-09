from flask import Flask, redirect, url_for
from routes.books import books_bp

app = Flask(__name__)

# Register the book routes
app.register_blueprint(books_bp)


@app.route('/')
def index():
    # Redirect root to the search page
    return redirect(url_for('books.search_books'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)