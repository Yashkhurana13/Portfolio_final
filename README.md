# Portfolio Website

A professional, mobile-responsive portfolio website built with Django, featuring a modern UI with Inter & JetBrains Mono fonts, cyan-emerald-teal color scheme, and enterprise-grade design patterns.

**Live URL:** [Add your deployment URL here]

## ✨ Features

- 🎨 **Professional Design** - Enterprise-grade UI with refined typography and color scheme
- 📱 **Fully Responsive** - Mobile-first design with hamburger menu
- 💼 **Complete Portfolio** - Profile, Skills, Projects, Experience, Achievements, Certificates, Blog
- ⚡ **Smooth Animations** - Purposeful micro-interactions and scroll animations
- 🔍 **SEO Optimized** - Proper meta tags and semantic HTML
- 🎯 **Admin Dashboard** - Easy content management via Django Admin

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Yashkhurana13/Portfolio_final.git
cd Portfolio_final
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📦 Deployment

### Deploy to Heroku

1. **Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Windows/Mac - Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-portfolio-name
```

4. **Set up PostgreSQL (recommended for production)**
```bash
heroku addons:create heroku-postgresql:mini
```

5. **Configure environment variables**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

6. **Deploy**
```bash
git push heroku main
```

7. **Run migrations on Heroku**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to Railway

1. **Connect GitHub repository**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `Portfolio_final`

2. **Add PostgreSQL**
   - In Railway dashboard, add PostgreSQL database
   - Railway will auto-detect Django and configure environment

3. **Set environment variables**
   - `DEBUG=False`
   - `SECRET_KEY` (generate a secure key)
   - `ALLOWED_HOSTS` (your Railway domain)

4. **Deploy**
   - Railway will automatically deploy on push to main branch

### Deploy to Render

1. **Create new Web Service**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn portfolio.wsgi`
   - Add PostgreSQL database

3. **Set environment variables**
   - `DATABASE_URL` (from Render PostgreSQL)
   - `SECRET_KEY`
   - `DEBUG=False`

4. **Deploy**
   - Render will automatically deploy

## 🛠️ Tech Stack

- **Backend:** Django 4.2
- **Frontend:** Tailwind CSS, Vanilla JavaScript
- **Fonts:** Inter, JetBrains Mono (Google Fonts)
- **Database:** SQLite (dev), PostgreSQL (production)
- **Deployment:** Gunicorn, WhiteNoise

## 📁 Project Structure

```
Portfolio_final/
├── apps/
│   ├── core/           # Main app (Profile, Skills, Projects, etc.)
│   └── blog/           # Blog functionality
├── portfolio/          # Django project settings
├── templates/          # HTML templates
├── static/            # CSS & JS files
├── media/             # Uploaded files
├── manage.py
├── requirements.txt
├── Procfile           # For Heroku deployment
└── README.md
```

## 🎨 Customization

### Update Profile Information

1. Access Django Admin: `/admin`
2. Login with superuser credentials
3. Update sections:
   - Profile (name, title, bio, social links)
   - Skills
   - Projects
   - Experience
   - Achievements
   - Certificates
   - Blog posts

### Change Colors

Edit `templates/base.html` and `static/css/style.css` to customize the color scheme.

### Update Fonts

Modify the Google Fonts link in `templates/base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Environment Variables

For production, set these environment variables:

- `SECRET_KEY` - Django secret key (generate using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Your domain(s)
- `DATABASE_URL` - PostgreSQL connection string (if using)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Yash Khurana - [Your Email]

Project Link: https://github.com/Yashkhurana13/Portfolio_final

---

⭐ Star this repository if you found it helpful!
