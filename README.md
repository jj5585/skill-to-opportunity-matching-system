# SkillSync – Setup & Run Guide

## Project Structure

```
skillsync/
├── manage.py
├── requirements.txt
├── .env.example
├── skillsync/                  # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/               # Users, Profiles, Skills, UserSkills
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── dashboard_views.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   ├── api_views.py
│   │   ├── urls.py
│   │   ├── api_urls.py
│   │   ├── dashboard_urls.py
│   │   ├── admin.py
│   │   └── management/commands/seed_skills.py
│   ├── opportunities/          # Opportunities, OpportunitySkills
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   ├── api_views.py
│   │   ├── urls.py
│   │   ├── api_urls.py
│   │   └── admin.py
│   └── matching/               # Matching engine + results
│       ├── models.py
│       ├── services.py         ← Core algorithm lives here
│       ├── views.py
│       ├── serializers.py
│       ├── api_views.py
│       ├── urls.py
│       └── api_urls.py
└── templates/
    ├── base.html
    ├── accounts/
    ├── opportunities/
    ├── matching/
    └── dashboard/
```

---

## Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip

---

## Step 1: Clone / Unzip the Project

```bash
cd /path/to/your/projects
# If cloning from git:
git clone <repo-url> skillsync
cd skillsync
```

---

## Step 2: Create & Activate Virtual Environment

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=skillsync_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

## Step 5: Create MySQL Database

```bash
mysql -u root -p
```

```sql
CREATE DATABASE skillsync_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

## Step 6: Run Migrations

```bash
python manage.py makemigrations accounts opportunities matching
python manage.py migrate
```

---

## Step 7: Seed Skills

```bash
python manage.py seed_skills
```

This populates 50+ common skills (Python, React, Docker, etc.).

---

## Step 8: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Use an email address as the username.

---

## Step 9: Run the Development Server

```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## User Flows

### Job Seeker
1. Register at `/accounts/register/` → select role **Job Seeker**
2. Go to **My Skills** → add skills with proficiency levels
3. Go to **My Matches** → see ranked opportunities
4. Click any match for a full skill-by-skill breakdown

### Recruiter
1. Register at `/accounts/register/` → select role **Recruiter**
2. Dashboard → **Post New Opportunity**
3. Add required skills with required proficiency levels
4. Click **View Candidates** on any posted opportunity to see ranked applicants

### Admin
- Access `/admin/` to manage all data

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Register user |
| GET/PATCH | `/api/accounts/me/` | Current user profile |
| GET | `/api/accounts/skills/` | List all master skills |
| GET/POST | `/api/accounts/my-skills/` | List / add user skills |
| GET/PATCH/DELETE | `/api/accounts/my-skills/<pk>/` | Manage one user skill |
| GET/POST | `/api/opportunities/` | List / create opportunities |
| GET/PATCH/DELETE | `/api/opportunities/<pk>/` | Opportunity detail |
| GET/POST | `/api/opportunities/<pk>/skills/` | Required skills for opportunity |
| GET | `/api/matching/my-matches/` | Ranked matches for current user |
| GET | `/api/matching/candidates/<opp_pk>/` | Ranked candidates for opportunity |

---

## Matching Algorithm

```
Proficiency Scores:
  Beginner     = 1 pt
  Intermediate = 2 pts
  Advanced     = 3 pts

For each required skill:
  User level >= Required level  →  full score  (required_score)
  User level <  Required level  →  half score  (required_score ÷ 2)
  Skill not in profile          →  0 pts

Match % = (User Total Score / Max Possible Score) × 100

Results sorted by Match % descending.
```

See `apps/matching/services.py` for the full implementation.

---

## Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set a strong `SECRET_KEY`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Run `python manage.py collectstatic`
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Put Nginx in front
- [ ] Enable HTTPS / SSL
- [ ] Use environment-specific MySQL credentials
