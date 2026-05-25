# Portfolio Backend & Architecture

A production-grade Django backend serving a professional developer portfolio. It is engineered with high performance, strict security, and clean architecture in mind, fully equipped for scalable cloud deployments.

## 🚀 Key Features

* **Dynamic Portfolio Engine**: Manage projects, skills, education, and experience through an intuitive admin panel.
* **Integrated Blog**: Full markdown/HTML compatible blog engine with automated image optimization.
* **Visitor Analytics**: Lightweight, privacy-first custom analytics middleware to track daily unique visitors and traffic without massive third-party scripts.
* **High-Performance Asset Pipeline**: 
  * AWS S3 integration for seamless cloud media storage.
  * `Pillow`-based automatic image resizing and compression on upload.
  * WhiteNoise integration for lightning-fast static file delivery.
* **Production Security**: Strict `SECRET_KEY` handling, HSTS, Secure Cookies, CSRF protection, and endpoint lockdown.

## 🛠️ Tech Stack

* **Backend Framework**: Django 4.2+ (Python 3.12)
* **Database**: PostgreSQL (Production) / SQLite (Local)
* **Cloud Storage**: Amazon S3 (boto3, django-storages)
* **Server**: Gunicorn, WSGI
* **Security & Optimization**: WhiteNoise, Pillow, Bleach, django-cors-headers

## 📦 Installation & Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yashkhurana13/Portfolio_final.git
   cd Portfolio_final
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Create a `.env` file in the root directory:
   ```env
   DJANGO_SECRET_KEY=your_local_secret_key
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   # Optional: Database URL for local postgres
   # DATABASE_URL=postgres://user:password@localhost:5432/portfolio
   ```

4. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## ☁️ Deployment Architecture

This project is built to deploy seamlessly on PaaS providers like Render/Heroku or classic EC2/Nginx instances.

### Required Production Environment Variables:
* `DJANGO_SECRET_KEY`: Long, cryptographically secure string.
* `DJANGO_DEBUG`: Set strictly to `False`.
* `DATABASE_URL`: Your PostgreSQL connection string.
* `DJANGO_ALLOWED_HOSTS`: Your production domains (comma-separated).

### AWS S3 Media Configuration (Required for Production):
* `AWS_STORAGE_BUCKET_NAME`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_S3_REGION_NAME`

The `build.sh` script automates dependency installation, static collection, and database migrations during the cloud deployment lifecycle.

## 🔒 Security & Analytics Notes

* **Privacy**: Visitor analytics hash IP addresses daily using SHA-256. Raw IPs are never permanently stored in the database.
* **Security**: The admin portal and critical endpoints are strictly locked behind `is_superuser` and `@login_required` decorators.

---
*Developed by Yash Khurana.*
