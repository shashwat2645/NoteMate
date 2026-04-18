# NoteMate

A modern, secure note-taking web application built with Django. NoteMate allows users to create, manage, and organize their personal notes with a clean, intuitive interface.

## Features

- **User Authentication**: Secure registration and login system
- **Email Verification**: OTP-based email verification for account security
- **Password Reset**: Secure password recovery via email
- **Note Management**: Full CRUD operations for notes (Create, Read, Update, Delete)
- **Dashboard**: Overview of recent notes and quick navigation
- **Responsive Design**: Modern UI built with Tailwind CSS
- **SQLite Database**: Lightweight database for development and small-scale deployment

## Tech Stack

- **Backend**: Django 6.0+
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS
- **Email**: SMTP support for notifications

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd notemate
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with the following variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@notemate.com
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

1. **Register**: Create a new account with email verification
2. **Verify Email**: Check your email for OTP and verify your account
3. **Login**: Access your dashboard
4. **Create Notes**: Add new notes with title and content
5. **Manage Notes**: View, edit, or delete your notes
6. **Dashboard**: See your recent notes and navigate quickly

## Project Structure

```
notemate/
├── accounts/          # User authentication app
│   ├── models.py      # User profile with email verification
│   ├── views.py       # Auth views (register, login, verify)
│   ├── forms.py       # Registration and login forms
│   ├── emails.py      # Email sending utilities
│   └── templates/     # Auth-related templates
├── notes/             # Notes management app
│   ├── models.py      # Note model
│   ├── views.py       # CRUD operations for notes
│   └── templates/     # Note-related templates
├── notemate/          # Main project settings
│   ├── settings.py    # Django configuration
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI configuration
├── templates/         # Global templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User-uploaded files
├── requirements.txt   # Python dependencies
├── manage.py          # Django management script
└── build.sh           # Build script for deployment
```

## API Endpoints

- `/` - Home (redirects to login/dashboard)
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/verify-email/` - Email verification
- `/dashboard/` - User dashboard
- `/notes/` - List all notes
- `/notes/create/` - Create new note
- `/notes/<id>/` - View note details
- `/notes/<id>/edit/` - Edit note
- `/notes/<id>/delete/` - Delete note

## Deployment

For production deployment:

1. Set `DEBUG=False` in your environment
2. Configure proper `ALLOWED_HOSTS`
3. Set up a production email backend
4. Use a production database (PostgreSQL recommended)
5. Run the build script: `./build.sh`
6. Deploy with Gunicorn or similar WSGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support or questions, please open an issue on the GitHub repository.
