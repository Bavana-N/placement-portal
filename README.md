# PlacePro — Premium Placement Portal (Django)

A complete, dynamic Placement Portal built with Python Django, Bootstrap 5, HTML5/CSS3,
and vanilla JavaScript. No React/Vue/Tailwind/DRF — pure Django MVT.

## Tech Stack
- Python Django 6 (Models, Views, Templates, Admin)
- SQLite (default database)
- Bootstrap 5 + Bootstrap Icons (via CDN)
- Google Fonts (Poppins)
- Vanilla JavaScript (scroll reveal, counters, back-to-top, loader)

## Project Structure
```
PlacementPortal/
├── manage.py
├── requirements.txt
├── placement_portal/       # Project settings, urls, wsgi/asgi
├── portal/                 # Main app: models, views, urls, admin, forms
│   └── management/commands/seed_data.py   # Demo data seeder
├── templates/
│   ├── base.html
│   └── portal/              # All 13 page templates
├── static/
│   ├── css/style.css        # Single premium stylesheet
│   └── js/script.js
└── media/                   # Uploaded resumes, logos, profile pics
```

## Database Models
- **Company** — name, industry, location, rating, website, about, etc.
- **Job** — ForeignKey to Company; title, salary range, skills, eligibility, type
- **Application** — links a User + Job; resume, cover letter, status
- **Announcement** — title, description, importance flag
- **AptitudeTest** — category, difficulty, duration, question count
- **ContactMessage** — contact form submissions
- **StudentProfile** — extends User with phone, college, resume, photo

## Setup & Run Instructions

```bash
# 1. Extract the zip and move into the project folder
cd PlacementPortal

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) Load demo companies, jobs, announcements & aptitude tests
python manage.py seed_data

# 6. Create an admin/superuser account
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver

# 8. Open in your browser
http://127.0.0.1:8000/            → Public site
http://127.0.0.1:8000/admin/      → Admin panel
```

## Pages Included
Home · About · Companies · Company Detail · Job Opportunities · Apply Job ·
Dashboard · Login · Register · Contact · Announcements · Aptitude Tests · 404

## Notes
- Media uploads (resumes, logos, profile pictures) are stored under `media/`.
- The custom `style.css` contains all variables, animations, gradients, and
  responsive breakpoints described in the design brief (glassmorphism navbar,
  24px rounded cards, gradient buttons, scroll-reveal, animated counters).
- Run `python manage.py seed_data` any time to (re)populate demo content —
  it uses `get_or_create` so it's safe to run multiple times.
- To reset the database, delete `db.sqlite3` and re-run steps 4–6.
