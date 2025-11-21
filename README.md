<div align="center">

# 🧠 AI Book – The Future of Knowledge Store
### "Designed for the Architects of the Future"

***

[![Tech: Django](https://img.shields.io/badge/Backend-Django%205.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![API: DRF](https://img.shields.io/badge/API-Django%20REST%20Framework-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Language: Python](https://img.shields.io/badge/Language-Python%203.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Frontend: HTML/CSS](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

***
</div>

<br>

## 🚀 About This Project

**AI Book (AI Learn)** is a cutting-edge e-commerce platform designed for selling educational resources, books, and AI courses. It bridges the gap between a classic Django web application and a modern API-driven architecture.

Unlike simple templates, this project demonstrates a scalable structure using **Django REST Framework (DRF)** alongside standard Django templates, creating a seamless experience for the "Architects of the Future".

**Key Objectives:**
- A robust **E-commerce Engine** for digital/physical products.
- **Hybrid Architecture:** Serving both Server-Side Rendered (SSR) pages and RESTful APIs.
- **Modern UI:** A clean, futuristic interface tailored for tech enthusiasts.

<br>

### 📬 Author & Repository

| Type | Link |
| :--- | :--- |
| 👤 **Author** | [Sina Jokar](https://github.com/sinajokarr) |
| 📦 **Repository** | [`Ai_Book`](https://github.com/sinajokarr/Ai_Book) |
| 💼 **LinkedIn** | [Sina Jokar](https://www.linkedin.com/in/sinajokar/) |

---

## 🛠️ Tech Stack: Under the Hood

A breakdown of the technologies powering the AI Book platform.

### ⚙️ Backend & API

| Component | Technology |
| :--- | :--- |
| **Core Framework** | `Django 5.x` |
| **API Framework** | `Django REST Framework (DRF)` |
| **Database** | `SQLite` (Dev) / PostgreSQL (Ready) |
| **Authentication** | Custom User Model + Django Auth System |

### 🎨 Frontend & UI

| Component | Technology |
| :--- | :--- |
| **Templating** | Django Template Language (DTL) |
| **Styling** | Custom CSS (`courses.css`, `books.css`) |
| **Interactivity** | Vanilla JavaScript |
| **Design Philosophy** | Minimalist, Futurism, Clean Typography |

---

## 💻 Project Features

### 📚 Product Management
- **Dynamic Listings:** Specialized views for `Books` and `Courses`.
- **Categorization:** Filter products by categories (AI, Data Science, Programming).
- **Rich Details:** Detailed product pages with pricing, descriptions, and metadata.

### 🛒 Shopping Experience
- **Smart Cart System:** Add/Remove items seamlessly.
- **Session Management:** Persistent cart data for non-logged-in users.
- **Order Processing:** From cart to checkout flow.

### 🔐 Security & Accounts
- **Custom User Model:** tailored for scalability (replacing the default Django user).
- **Secure Authentication:** Login, Signup, and Logout functionality.
- **CSRF Protection:** Full security compliance for forms.

---

## 🧱 Project Structure

A simplified view of the `store_drff` architecture:

```bash
Ai_Book/
├── config/               # Core project settings and main URLs
│   ├── settings.py
│   └── urls.py
├── core/                 # Shared utilities and base models
├── store/                # Main E-commerce Logic
│   ├── models.py         # Product, Category, Cart, Order models
│   ├── views.py          # Business logic for store pages
│   ├── serializers.py    # DRF Serializers for API transformation
│   ├── urls.py           # Store routing
│   └── templates/store/  # HTML Templates (about, contact, lists)
├── static/               # Static assets (CSS, Images, JS)
│   └── store/
│       ├── css/          # Custom styles
│       └── images/       # Product assets
├── templates/            # Base templates
│   └── _base.html        # Master layout (Header/Footer)
└── manage.py             # Django command-line utility
⚙️ Installation & Setup Guide
Follow these steps to run the project locally on your machine.

Bash
# 1. Clone the repository
git clone [https://github.com/sinajokarr/Ai_Book.git](https://github.com/sinajokarr/Ai_Book.git)
cd Ai_Book

# 2. Create a Virtual Environment
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Install Dependencies
pip install django djangorestframework

# 4. Apply Database Migrations
python manage.py migrate

# 5. Create a Superuser (Admin)
python manage.py createsuperuser

# 6. Run the Server
python manage.py runserver
🌍 Access the App

Open your browser and navigate to:

http://127.0.0.1:8000/

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

<div align="center">

Build the Future. © 2025 AI Learn.

</div>
