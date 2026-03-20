# 🐍 Flask + MongoDB — User Auth

Web app built with Python, Flask and MongoDB Atlas. Covers user registration and login with persistent storage using pymongo.

Built as a teaching project for a Python + Flask + NoSQL course.

---

## 🚀 Features

- User registration with duplicate email validation
- Login with credential verification against MongoDB
- Jinja2 templates with Bootstrap styling
- Blueprint-based route organization
- MongoDB Atlas as cloud database

---

## 🗂️ Project Structure

```
project/
├── app.py               # Routes and Flask logic
├── mongo_config.py      # MongoDB connection
└── templates/
    ├── templates.html   # Base template + navbar
    ├── home.html        # Welcome page
    ├── login.html       # Login form
    └── register.html    # Register form
```

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install flask pymongo[srv]
```

**4. Configure MongoDB**

Create a free cluster at [cloud.mongodb.com](https://cloud.mongodb.com), then update `mongo_config.py` with your connection string:

```python
MONGO_URI = "mongodb+srv://YOUR_USER:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/"
```

**5. Run the app**
```bash
python app.py
```

App runs at `http://localhost:5000`

---

## 📌 Available Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/login` | GET / POST | Login form |
| `/register` | GET / POST | Registration form |
| `/inicio` | GET | Inicio page |

---

## ⚠️ Notes

- Passwords are stored in **plain text** — this is intentional for learning purposes only.
- For production use, hash passwords with `bcrypt` and store credentials in environment variables.

---

## 🛠️ Tech Stack

- [Python 3](https://python.org)
- [Flask](https://flask.palletsprojects.com)
- [pymongo](https://pymongo.readthedocs.io)
- [MongoDB Atlas](https://cloud.mongodb.com)
- [Bootstrap 5](https://getbootstrap.com)
