# PlacementVault

A full-stack Django web app that helps students prepare for campus placements
by letting them **schedule upcoming interviews** and **read (and share)
company-wise interview experiences** from other students.

Built with server-rendered Django templates and plain CSS only — no React,
no REST API layer, no JavaScript framework, no Bootstrap.

## Why this exists

Two recurring problems during placement season:

1. Students lose track of which company/round is coming up when.
2. Genuine, company-specific interview experiences are scattered or hard to find.

PlacementVault solves both with two simple modules: a personal **Schedule**
and a shared, searchable pool of **Experiences**.

## Tech stack

| Layer          | Choice                                   |
|-----------------|-------------------------------------------|
| Backend         | Python, Django                            |
| Database (dev)  | SQLite (zero setup)                       |
| Database (prod) | PostgreSQL, via `DATABASE_URL`            |
| Frontend        | Django Templates, plain HTML/CSS          |
| Auth            | Django's built-in `User` model            |
| Static files    | WhiteNoise                                |
| Deployment      | Render, Gunicorn                          |

## Features

- **Auth** — register, login, logout, using Django's built-in auth
- **Dashboard** — total scheduled interviews, total published experiences, upcoming interviews at a glance
- **Schedule** — add / view / edit / delete your own upcoming interviews (company, role, round, date, time)
- **Publish Experience** — add / view / edit / delete interview experiences you've shared (company, role, round, focus subject, full write-up)
- **Search** — drill down through **Company → Role → Round → Experiences** to read what other students went through for a specific interview
- **Role suggestions** — an HTML `<datalist>` suggests common roles while typing, but any custom role can be entered — no JavaScript required
- **Data normalization** — company/role/round text is trimmed and title-cased on save, so "infosys", "INFOSYS", and "Infosys" don't fragment into separate search branches

## Security notes

- Every view that touches a user's own data (`schedule_edit`, `schedule_delete`,
  `experience_edit`, `experience_delete`, etc.) filters the database lookup by
  `user=request.user`, not just by ID. This means visiting another user's
  record URL directly returns a 404, not their data — ownership is enforced
  at the query level, not only by `@login_required`.
- CSRF protection is on by default on every form (Django's built-in middleware).
- Passwords are validated and hashed by Django's built-in auth system — never
  stored in plain text.

## Getting started locally

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd PlacementVault

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations (creates db.sqlite3 automatically)
python manage.py makemigrations
python manage.py migrate

# 5. (Optional) create an admin account to browse data at /admin/
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — you'll land on the login page. Register a
new account to get started.

No `.env` file is required to run locally — see `.env.example` for the
optional environment variables and what they control.

## Deploying to Render

1. Push this project to a GitHub repository.
2. On Render, create a **PostgreSQL** database first, and copy its internal
   connection string.
3. Create a **Web Service** pointing at your repo, with:
   - **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start command:** `gunicorn core.wsgi`
4. Add environment variables on the web service:
   - `SECRET_KEY` — any long random string
   - `DEBUG` — `False`
   - `DATABASE_URL` — the PostgreSQL connection string from step 2
   - `ALLOWED_HOSTS` — your Render URL, e.g. `placementvault.onrender.com`
5. Deploy. Render sets `RENDER_EXTERNAL_HOSTNAME` automatically, which
   `core/settings.py` also allows.

## Project structure

```
PlacementVault/
├── core/                  # Django project: settings, root URLs, WSGI
├── placementvault/        # The app: models, views, forms, URLs, admin
│   └── migrations/
├── templates/             # All HTML templates (server-rendered)
│   └── registration/      # login.html, register.html
├── static/css/style.css   # The entire design system — one plain CSS file
├── manage.py
├── requirements.txt
├── Procfile                # Tells Render/Heroku how to start the app
├── .env.example
└── README.md
```

## Design notes

The visual language leans into the subject itself — placement season is full
of admit cards, ledgers, and stamped official documents — rather than a
generic dashboard look. Interview rounds and focus subjects are shown as
small stamped badges; schedule/experience rows are styled like ledger
entries. No design framework is used; every rule in `style.css` is
hand-written and grouped by component.

## Known limitations / possible next steps

This is an honest snapshot of what's *not* built yet, so it doesn't come as
a surprise in an interview:

- **No automated tests yet.** Manually verified: register → login → add
  schedule → edit → delete, and the same for experiences, plus the full
  search drill-down. Worth adding `pytest-django` tests before treating this
  as production-ready.
- **No reminders or notifications.** Originally scoped as a future
  enhancement, not part of this build.
- **Search matches on exact normalized text**, not fuzzy matching — e.g. a
  role has to match the stored value exactly (after trim + title-case) to
  appear grouped together.
- **No pagination** on the search results or list pages — fine at small
  scale, would need it if experience volume grows significantly.
