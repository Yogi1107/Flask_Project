from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'library.db'

# ---------------------------
# Initialize Database
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Books table
    c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        available_copies INTEGER NOT NULL
    )
    ''')

    # Members table
    c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    # Borrows table
    c.execute('''
    CREATE TABLE IF NOT EXISTS borrows (
        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

init_db()

# ---------------------------
# Home Page
# ---------------------------
@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM books")
    books = c.fetchall()

    c.execute("SELECT * FROM members")
    members = c.fetchall()

    c.execute('''
    SELECT b.borrow_id, bk.title AS book_title, m.name AS member_name, b.borrow_date
    FROM borrows b
    JOIN books bk ON b.book_id = bk.book_id
    JOIN members m ON b.member_id = m.member_id
    WHERE b.return_date IS NULL
    ''')
    borrows = c.fetchall()

    conn.close()
    return render_template('index.html', books=books, members=members, borrows=borrows)

# ---------------------------
# Add/Edit/Delete Books
# ---------------------------
@app.route('/add_books', methods=['GET','POST'])
def add_books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        available_copies = request.form['available_copies']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO books (title, author, available_copies) VALUES (?, ?, ?)',
                  (title, author, available_copies))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_books.html')

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
    book = c.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        available_copies = request.form['available_copies']
        c.execute('UPDATE books SET title = ?, author = ?, available_copies = ? WHERE book_id = ?',
                  (title, author, available_copies, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Optional: prevent deletion if currently borrowed
    c.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ---------------------------
# Add/Edit/Delete Members
# ---------------------------
@app.route('/add_members', methods=['GET','POST'])
def add_members():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO members (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_members.html')

@app.route('/edit_member/<int:member_id>', methods=['GET','POST'])
def edit_member(member_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
    member = c.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        c.execute('UPDATE members SET name = ?, email = ? WHERE member_id = ?', (name, email, member_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_member.html', member=member)

@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM members WHERE member_id = ?', (member_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ---------------------------
# Borrow & Return Books
# ---------------------------
@app.route('/borrow_book', methods=['GET','POST'])
def borrow_book():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE available_copies > 0")
    books = c.fetchall()
    c.execute("SELECT * FROM members")
    members = c.fetchall()
    conn.close()

    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO borrows (book_id, member_id, borrow_date) VALUES (?, ?, ?)',
                  (book_id, member_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        c.execute('UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?', (book_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('borrow_book.html', books=books, members=members)

@app.route('/return_book', methods=['GET','POST'])
def return_book():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
    SELECT b.borrow_id, bk.title AS book_title, m.name AS member_name
    FROM borrows b
    JOIN books bk ON b.book_id = bk.book_id
    JOIN members m ON b.member_id = m.member_id
    WHERE b.return_date IS NULL
    ''')
    borrows = c.fetchall()
    conn.close()

    if request.method == 'POST':
        borrow_id = request.form['borrow_id']
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('UPDATE borrows SET return_date = ? WHERE borrow_id = ?',
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), borrow_id))
        c.execute('UPDATE books SET available_copies = available_copies + 1 WHERE book_id = (SELECT book_id FROM borrows WHERE borrow_id = ?)', (borrow_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('return_book.html', borrows=borrows)

# ---------------------------
# Run Flask App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
