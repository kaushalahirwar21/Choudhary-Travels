# 🚗 Choudhary Travels - Car Booking System

This is a full-stack Django project built for online car booking.

## 📌 Project Purpose

- Provide fast and easy ride booking experience for users
- Allow vehicle owners/admins to manage schedules, bookings, and pricing
- Auto price calculation, booking conflict prevention, and WhatsApp notifications

## 🌟 Key Features

1. User registration and login (Django Auth)
2. Car availability and booking calendar
3. Automatic time-based pricing
4. Duplicate booking check (conflict detection)
5. WhatsApp notifications (booking confirmation)
6. Admin dashboard (car and booking management)
7. Car image upload support
8. Responsive UI (mobile + desktop)
9. Modern UI animations (AOS)
10. SQLite DB with Django ORM

## 🛠️ Technology Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap, JavaScript
- Database: SQLite
- Deployment target: Render

## 📁 Project Structure

- `booking/` - Django app (models, views, admin, template tags)
- `config/` - Django config (settings, urls, wsgi, asgi)
- `templates/` - HTML templates
- `static/` - static assets, CSS, images
- `db.sqlite3` - local database

<img width="1847" height="862" alt="image" src="https://github.com/user-attachments/assets/3609b66c-f3ba-4684-8533-8e040bfef70e" />
 

## 🚀 Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/kaushalahirwar21/choudhary-travels.git
   cd choudhary-travels
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start server:
   ```bash
   python manage.py runserver
   ```
7. Open browser:
   - `http://127.0.0.1:8000/` (home page)
   - `http://127.0.0.1:8000/admin/` (admin panel)

## 🧪 Testing

```bash
python manage.py test
```

## 🔧 Configuration

- Check `config/settings.py` for `ALLOWED_HOSTS`, `DATABASES`, `STATIC_URL`, and email/WhatsApp settings
- Set WhatsApp API key/number in `booking/views.py` or a dedicated service module used by the integration

## 📌 User Guide

1. Browse available cars on the home page
2. Pick required date/time and make a booking
3. System blocks conflicting time overlaps
4. Successful booking triggers WhatsApp notification

## 🛡️ Security and Optimization

- User authentication and form validation
- CSRF protection enabled by Django
- Model-level checks for booking constraints

## 📸 Screenshots

(Add screenshots here after deployment / local run)

## 📝 Contributing

- Fork the repo
- Create a feature branch
- Open a pull request
- Follow code style (PEP8 / Black)

## 📄 License

MIT License (or your preferred license)

## 📬 Contact

- GitHub: `https://github.com/kaushalahirwar21/choudhary-travels`
- Email: kaushalahirwar714@gmail.com
- contact : 9977949032

## Render Deployment

1. Push this project to a GitHub repository.
2. In Render, create a new Blueprint and select that repository.
3. Render will detect `render.yaml` and create:
   - one Python web service
   - one PostgreSQL database
4. After the first deploy, open the Render shell and create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Visit the generated `onrender.com` URL.
