# Swappily

**Swappily** is a modern, AI-powered skill-swapping platform designed to connect people who want to learn through mutual exchange. Instead of paying with money, users trade their expertise, creating a collaborative learning environment.

## 🚀 Key Features

- **Skill Listing**: Users can showcase their expertise with detailed descriptions and images.
- **Swap Requests**: Intuitive system to request a "swap" between two skills, including options to attach introductory videos or PDFs.
- **Real-time Notifications**: Stay updated on request approvals, rejections, and new messages via structured system notifications.
- **Dynamic Branding**: UI colors are driven by CSS variables injected from the backend, ensuring brand consistency.
- **Multi-language Support**: Full RTL/LTR support for Arabic, English, and French.
- **AJAX-First Interaction**: Optimized user experience with translatable SweetAlert2 feedback and seamless form handling.

## 📊 Database Schema

The database schema visualization has been moved to [diagram.drawio](file:///home/mohamed/github/swappily/diagram.drawio). You can open it using the Draw.io integration in your editor.

## 🛠️ Tech Stack

- **Backend**: Django 5.2+
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Environment**: python-decouple for secure configuration.
- **Styling**: Bootstrap 5.3 + Custom CSS Variables.
- **UI/UX**: SweetAlert2 for dynamic user feedback.

## 🛠️ Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/amraoui-mo7amed/swappily
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure your settings.
```bash
cp .env.example .env
```

**Generate a Secret Key:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Database Migration
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

## 📖 Development Guide

### AJAX Form Handling
The project uses a centralized JavaScript handler for any form with the `.form` class. Return a `JsonResponse` from your view:

```python
return JsonResponse({
    "success": True,
    "message": _("Skill added successfully!"),
    "redirect_url": "/dashboard/"
})
```

## 📄 License
This project is developed for educational and collaborative learning purposes.

