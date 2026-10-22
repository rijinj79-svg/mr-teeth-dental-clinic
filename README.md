# Mr.Teeth Multispeciality Dental Clinic

A Django clinic website with public clinic pages, patient appointments, staff tools, and administrator-managed content.

## Features
- Public clinic pages with Bootstrap icons and the requested High Tower Text font family (when installed on the visitor's device).
- Patient registration/login, dashboard and appointment history.
- Appointment requests with date/time and doctor selection, plus staff-entered walk-in appointments that do not require a patient website account.
- Staff-only appointment, patient-record, enquiry and finance workflows.
- Administrator-only creation and activation/deactivation of staff accounts. Public administrator registration is disabled.
- Administrator-managed doctor profiles and photos, image/video gallery uploads, and visitor-feedback moderation.
- Public feedback submission without login; feedback is shown only after administrator approval.
- Media uploads stored under `media/` during local development.

## Windows setup

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Sign in with the superuser using the custom Admin Login page. From Admin Dashboard, create staff accounts; those accounts can then use Staff Login. Do not create staff accounts through public registration.

## Database and deployment notes

This project settings file currently targets a local MySQL database named `mrteeth_db`. Ensure the MySQL service is running and set the correct database credentials before running migrations. Keep passwords and secret keys in environment variables and never upload them to a public repository.

For public deployment, configure `DEBUG=False`, production `ALLOWED_HOSTS`, HTTPS, a production database, secure environment variables, email credentials, media storage/backups, and a real domain. User-uploaded videos can consume substantial storage; configure an upload-size limit and appropriate hosting storage for production.
