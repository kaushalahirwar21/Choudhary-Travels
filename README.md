# 🚗 Choudhary Travels - Car Booking System
This is a full-stack Django project built for online car booking.

## 📌 Project Purpose
- Provide fast and easy ride booking experience for users
- Allow vehicle owners/admins to manage schedules, bookings, and pricing
- Auto price calculation, booking conflict prevention, and WhatsApp notifications

## 🌟 Key Features
- User registration and login (Django Auth)
- Car availability and booking calendar
- Automatic time-based pricing
- Duplicate booking check (conflict detection)
- WhatsApp notifications (booking confirmation)
- Admin dashboard (car and booking management)
- Car image upload support
- Responsive UI (mobile + desktop)
- Modern UI animations
- SQLite DB with Django ORM

## 🛠️ Technology Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite (for development)
- **Deployment:** Vercel

## 📁 Project Structure
- `booking/` - Django app (models, views, admin, template tags)
- `config/` - Django config (settings, urls, wsgi)
- `templates/` - HTML templates
- `static/` - Static assets (CSS, images, JS)
- `vercel.json` - Vercel deployment configuration
- `build.sh` - Build script for Vercel

## 🚀 Run Locally
1.  **Clone the repo:**
    ```bash
    git clone <your-repository-url>
    cd choudhary-travels
    ```
2.  **Create virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Start server:**
    ```bash
    python manage.py runserver
    ```
7.  **Open in browser:**
    - Home: `http://127.0.0.1:8000/`
    - Admin: `http://127.0.0.1:8000/admin/`

## 🧪 Testing
```bash
python manage.py test
```

## 🔧 Vercel Deployment
This project is configured for easy deployment on Vercel.

1.  **Install the Vercel CLI:**
    ```bash
    npm install -g vercel
    ```
2.  **Deploy the project:**
    From the project root directory, run:
    ```bash
    vercel
    ```
3.  **Configure Environment Variables:**
    After deployment, add your production environment variables (from your `.env` file) in your Vercel project settings. This includes `DJANGO_SECRET_KEY`, `DATABASE_URL`, and any WhatsApp/Twilio credentials.

## 🛡️ Security and Optimization
- User authentication and form validation
- CSRF protection enabled by Django
- Model-level checks for booking constraints

## 📸 Screenshots
(Add screenshots here after deployment / local run)

## 📝 Contributing
1.  Fork the repo
2.  Create a feature branch
3.  Open a pull request
4.  Follow code style (PEP8 / Black)

## 📄 License
This project is under the MIT License.