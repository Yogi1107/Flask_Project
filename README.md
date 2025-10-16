# Flask Library Management System

This is a web application built with **Flask** for managing a small library's collection of books and tracking member borrowing activity. It provides a simple interface for librarians to add books, register members, and log book borrowing and returning.

---

## Features

* **Book Management:** Add new books, view the entire collection, and check book availability.
* **Member Management:** Register new library members.
* **Borrowing Tracking:** Log when a book is borrowed and returned, managing the loan status.
* **Database Storage:** Uses **SQLite** to persist book and borrowing data.
* **Web Interface:** Simple, templated user interface using HTML/CSS (in the `templates` and `static` folders).

---

## Technologies Used

| Technology | Description |
| :--- | :--- |
| **Python** | The core programming language for the backend logic. |
| **Flask** | A lightweight WSGI web application framework in Python. |
| **SQLite** | The file-based database used to store application data (`library.db` and `borrows.db`). |
| **HTML/CSS**| Used for the application's front-end structure and styling. |

---

## Installation and Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Yogi1107/Flask_Project.git](https://github.com/Yogi1107/Flask_Project.git)
cd Flask_Project
```

### 2. Set up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```Bash

# Create the environment
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
Since a requirements.txt is not provided, you will need to manually install Flask.
```
Bash
pip install Flask
```
(If the project uses other Python libraries, they should be listed and installed here.)

## ⚙️ Usage
1. Run the Application
Execute the main application file library_management.py:
Bash
```
python library_management.py
```
2. Access the Web App
Once the application is running, you will typically see output indicating the server address. Open your web browser and navigate to:

http://127.0.0.1:5000/

### 📄 License
This project is open-source. Please check the repository for a specific license file (e.g., LICENSE.md). If no explicit license is provided, standard GitHub public repository terms apply
