# Pharmacy Web Platform

This repository contains a Django REST + React/Vite foundation. Deployment and orchestration are intentionally not included; run PostgreSQL, Redis, and an S3-compatible service separately or configure equivalent managed services through environment variables.

## Local development

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Copy `backend/.env.example` to `backend/.env` and provide service credentials as needed.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

The API is documented at `/api/docs/` and `/api/schema/`.

## Demo data

After running migrations, populate the local database with repeatable demo data:

```powershell
python manage.py seed_demo
```

The command creates six medicines, four categories, three manufacturers, one approved
pharmacy, inventory stock, and two demo accounts:

| Role | Email | Password |
| --- | --- | --- |
| Customer | `customer@demo.pharmacy` | `DemoCustomer123!` |
| Pharmacy owner | `owner@demo.pharmacy` | `DemoOwner123!` |

Running `seed_demo` again updates the same records instead of creating duplicates.
