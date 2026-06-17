# Peter Charles Portfolio Platform

A production-ready Django portfolio website for a Data Analyst & Product Manager — Peter Charles.

## ✨ Features

- **10 Django apps**: core, projects, blog, services, training, testimonials, contact, bookings, dashboard, api
- **Full case study system** with project metrics, architecture, lessons learned
- **REST API** (DRF) at `/api/v1/`
- **HTMX contact form** with live success feedback
- **Three.js hero** — animated particle network + cyber grid
- **Glassmorphism dark UI** — Space Grotesk + JetBrains Mono
- **Skill bars**, counter animations, AOS scroll effects
- **Admin dashboard** at `/dashboard/`
- **Booking system** for consultation slots
- **Email notifications** via SMTP
- **Cloudinary** media storage (optional)
- **Docker + docker-compose** ready
- **Railway / Render / Heroku** deploy-ready (Procfile included)

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Clone & Install

```bash
git clone <your-repo>
cd peter_portfolio
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

```bash
cp .env.example .env
# Edit .env — the defaults work for local dev (SQLite, console email)
```

### 4. Database & Demo Data

```bash
python manage.py migrate
python manage.py seed_demo        # Populates all demo content
```

### 5. Run the Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

**Admin access**: http://127.0.0.1:8000/admin  
Username: `peter` | Password: `admin123`

---

## 🐳 Docker Compose (with PostgreSQL)

```bash
# Copy and configure env
cp .env.example .env

# Set USE_SQLITE=False and configure DB credentials in .env
docker-compose up --build

# In a second terminal:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_demo
```

---

## ☁️ Deploy to Railway

1. Push repo to GitHub
2. Create new Railway project → "Deploy from GitHub"
3. Add a PostgreSQL service in Railway
4. Set environment variables (copy from `.env.example`):
   - `SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_hex(50))"`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=yourapp.up.railway.app`
   - `USE_SQLITE=False`
   - `DATABASE_URL` — Railway provides this automatically
5. Railway will auto-detect the Procfile and run migrations on deploy

## ☁️ Deploy to Render

1. New Web Service → connect GitHub repo
2. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start command: `gunicorn config.wsgi:application`
4. Add PostgreSQL (Render provides free tier)
5. Set all environment variables from `.env.example`

## ☁️ Deploy to Heroku

```bash
heroku create peter-portfolio
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=... DEBUG=False ALLOWED_HOSTS=...herokuapp.com USE_SQLITE=False
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py seed_demo
```

---

## 📁 Project Structure

```
peter_portfolio/
├── config/              # Django settings, urls, wsgi
├── core/                # Home, about, skills, experience, certifications
│   └── management/commands/seed_demo.py
├── projects/            # Project portfolio with full case studies
├── blog/                # Blog with categories and tags
├── services/            # Professional services catalogue
├── training/            # Training programs with curriculum
├── testimonials/        # Client testimonials
├── contact/             # HTMX contact form
├── bookings/            # Consultation booking system
├── dashboard/           # Staff analytics dashboard
├── api/                 # REST API (DRF)
├── templates/           # HTML templates (extends base.html)
├── static/
│   ├── css/main.css     # Full cyber dark design system
│   └── js/
│       ├── main.js      # AOS, nav, skill bars, interactions
│       ├── particles.js # Three.js particle network
│       ├── hero3d.js    # Three.js hero grid + skill universe
│       └── counters.js  # Animated stat counters
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile
└── .env.example
```

---

## 🔧 Customisation

### Update Personal Info
Run `python manage.py seed_demo` after editing the seed command, or use the admin panel at `/admin/core/sitesettings/`.

### Add Projects
Admin → Projects → Add Project  
Fill in all case study fields for rich project detail pages.

### Change Colours
Edit `--cyan` in `static/css/main.css` `:root` block.

### Add Blog Posts
Admin → Blog → Posts → Add Post  
Set status to `published` for public visibility.

---

## 🛡️ Security Checklist (Production)

- [ ] Set `DEBUG=False`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set `USE_SQLITE=False` with PostgreSQL
- [ ] Configure Cloudinary for media
- [ ] Configure SMTP email
- [ ] Run `python manage.py check --deploy`

---

## 📄 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2+ |
| API | Django REST Framework |
| Frontend | Bootstrap 5, Three.js r128, GSAP 3, AOS |
| Forms | HTMX 1.9 |
| Fonts | Space Grotesk, JetBrains Mono |
| Icons | Font Awesome 6 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Media | Cloudinary / Local |
| Deploy | Railway / Render / Heroku / Docker |

---

Built with ❤️ in Abuja, Nigeria.
