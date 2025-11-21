<div align="center">

# 🧠 AI Book – The Future of Knowledge
### "Designed for the Architects of the Future"

***

[![Tech: Django](https://img.shields.io/badge/Backend-Django%205.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![API: DRF](https://img.shields.io/badge/API-Django%20REST%20Framework-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Language: Python](https://img.shields.io/badge/Language-Python%203.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Language: JavaScript](https://img.shields.io/badge/Scripting-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

***
</div>

<br>

## 🚀 About The Project

**AI Book** (also known as AI Learn) is a modern, scalable e-commerce platform dedicated to educational resources, including physical **Books** and digital **AI Courses**.

This project demonstrates a professional integration of **Django** (Server-Side Rendering) with **Django REST Framework (DRF)** and **JavaScript** interactivity. It goes beyond simple templates to offer a dynamic, "Quiet Luxury" user experience tailored for tech enthusiasts.

<br>

## ✨ Key Features

### 🛍️ E-Commerce Core
* **Dynamic Product Catalog:** specialized views for separating *Books* and *Courses*.
* **Smart Search & Filtering:** Filter products by Category, Price, or Date.
* **Cart System (AJAX):** Add/Remove items instantly using **JavaScript** without reloading the page.
* **Order Management:** Full flow from "Add to Cart" to "Checkout".

### 🔐 Authentication & Security
* **Custom User Model:** Extensible user architecture (replacing default Django user).
* **Secure Auth:** Signup, Login, and Logout flows styled with custom templates.
* **Role-Based Access:** Admin panel for managing products and orders.

### 🎨 Modern UI/UX
* **Responsive Design:** Fully adapted for Mobile, Tablet, and Desktop.
* **Interactive Elements:** JavaScript-powered sliders and cart counters.
* **Clean Aesthetic:** "Architects of the Future" design philosophy.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | `Django 5.x` | Core web framework |
| **API** | `DRF` | RESTful API integration (store_drff) |
| **Frontend Logic** | `JavaScript (ES6+)` | Cart interactivity & AJAX calls |
| **Templating** | `HTML5 / DTL` | Django Template Language |
| **Styling** | `CSS3` | Custom flexible layouts (Flexbox/Grid) |
| **Database** | `SQLite` | Development database (Swapable with PostgreSQL) |

---

## 🧱 Project Structure

Based on the `store_drff` architecture:

```bash
Ai_Book/
├── config/               # Project configuration (settings, main urls)
├── core/                 # Core utilities and base models
├── store/                # Main Application Logic
│   ├── models.py         # Product, Category, Order models
│   ├── views.py          # Business logic (CBVs)
│   ├── api_views.py      # DRF API endpoints
│   ├── serializers.py    # JSON serialization for API
│   ├── urls.py           # App routing
│   └── static/store/     # JS and CSS files
├── templates/            # Global HTML templates (_base.html)
├── db.sqlite3            # Local database
└── manage.py             # Django CLI tool
````

-----

## ⚙️ Installation & Setup

Follow these steps to get a local copy up and running.

### 1\. Clone the Repository

```bash
git clone [https://github.com/sinajokarr/Ai_Book.git](https://github.com/sinajokarr/Ai_Book.git)
cd Ai_Book
```

### 2\. Create Virtual Environment

```bash
python -m venv .venv
# Activate it:
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install django djangorestframework
```

### 4\. Database Setup

```bash
python manage.py migrate
```

### 5\. Create Admin User

```bash
python manage.py createsuperuser
```

### 6\. Run Server

```bash
python manage.py runserver
```

Open your browser and visit: **`http://127.0.0.1:8000/`**

-----

## 📬 Contact

**Sina Jokar** - Backend Developer & AI Enthusiast

  * **GitHub:** [github.com/sinajokarr](https://github.com/sinajokarr)
  * **Project Link:** [github.com/sinajokarr/Ai\_Book](https://www.google.com/search?q=https://github.com/sinajokarr/Ai_Book)

\<div align="center"\>

**Build the Future.**
© 2025 AI Learn.

\</div\>

