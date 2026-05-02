# Personal Finance Tracker

A production-ready Django web application for tracking personal finances with budgeting, reporting, and notifications.

## Features

### Core Features

- **User Authentication**: Registration, login/logout, and profile management
- **Google OAuth Integration**: Sign in with Google using django-allauth
- **Transaction Management**: Create, read, update, delete income and expense transactions
- **Multi-Currency Support**: Track transactions in any ISO 4217 currency (INR, USD, EUR, etc.)
- **Category Management**: Organize transactions with user-defined categories
- **Budgeting**: Set monthly budgets per expense category and track spending
- **Reports**: Monthly income vs expense reports and category-wise analysis
- **Notifications**: Email alerts when budgets are exceeded
- **Dashboard**: Real-time financial overview with key metrics

### Technical Features

- **PostgreSQL Database**: Production-grade relational database
- **Decimal Precision**: All monetary calculations use Python Decimal for accuracy
- **ORM Aggregation**: Efficient database queries for financial metrics
- **Class-Based Views**: Clean, modular view architecture
- **Environment Variables**: Secure configuration management
- **SendGrid Integration**: Ready for email notifications via SendGrid SMTP
- **Static Files**: WhiteNoise for efficient static file serving
- **Tests**: Comprehensive test suite for models, views, and business logic

## Tech Stack

- **Backend**: Python 3.x, Django 4.2
- **Database**: PostgreSQL 12+
- **API**: Django REST Framework (for future API extensions)
- **Authentication**: django-allauth with Google OAuth
- **Email**: SendGrid-compatible SMTP
- **Deployment**: gunicorn, daphne, whitenoise

## Project Structure

```
finance_tracker/
├── finance_tracker/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── accounts/                # User authentication & profiles
│   ├── models.py            # UserProfile model
│   ├── views.py             # Dashboard, profile views
│   ├── forms.py             # Profile forms
│   └── urls.py              # Auth routes
├── transactions/            # Income & expense tracking
│   ├── models.py            # Transaction, Category models
│   ├── views.py             # Transaction CRUD views
│   ├── forms.py             # Transaction forms
│   ├── admin.py             # Django admin configuration
│   └── urls.py              # Transaction routes
├── budgets/                 # Budget management & tracking
│   ├── models.py            # Budget model
│   ├── views.py             # Budget CRUD views
│   ├── forms.py             # Budget forms
│   ├── signals.py           # Budget overrun notifications
│   └── urls.py              # Budget routes
├── reports/                 # Financial reports & analytics
│   ├── views.py             # Monthly and category reports
│   └── urls.py              # Report routes
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── accounts/            # Account templates
│   ├── transactions/        # Transaction templates
│   ├── budgets/             # Budget templates
│   └── reports/             # Report templates
├── static/                  # Static files (CSS, JS)
├── manage.py                # Django management script
├── tests.py                 # Test suite
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # Readme file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip and virtualenv

### Step 1: Clone/Setup Project

```bash
cd finance_tracker
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-change-in-production
DB_NAME=finance_tracker
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Database Setup

Create PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE finance_tracker;

# Exit
\q
```

Run migrations:

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Step 8: Access Admin Panel

Visit `http://localhost:8000/admin/` and log in with your superuser credentials.

## Usage

### User Registration & Login

1. Navigate to `/accounts/signup/` to create a new account
2. Fill in email, username, and password
3. Optionally sign in with Google

### Creating Transactions

1. Go to Transactions > New Transaction
2. Select category, enter amount, date, and optional description
3. Upload receipt (optional)
4. Save

### Managing Categories

1. Go to Transactions > Categories
2. Create income and expense categories
3. Edit or delete as needed

### Setting Budgets

1. Go to Budgets > New Budget
2. Select an expense category
3. Set monthly limit
4. Save

You'll receive email notifications if you exceed a budget.

### Viewing Reports

1. **Monthly Report**: Income vs expenses broken down by month
2. **Category Report**: Income and expense totals by category

### Dashboard

The dashboard shows:

- Total income and expenses
- Current savings (income - expenses)
- Budget status with percentage used
- Recent transactions
- Budget alerts

## Database Models

### User Profile

- Extended user information with preferred currency
- Avatar support
- Biography

### Category

- User-specific income and expense categories
- Type: INCOME or EXPENSE
- Unique per user and type

### Transaction

- Income or expense records
- DecimalField for amount (10 digits, 2 decimal places)
- Optional file receipt upload
- Multi-currency support
- Timestamps for created and updated

### Budget

- Monthly spending limits per category
- OneToOne relationship with Category
- Tracks percentage used and overrun status

## API Endpoints (for future use)

The project uses Django REST Framework and is configured for API expansion:

- `/api/transactions/` - Transaction CRUD operations
- `/api/budgets/` - Budget management
- `/api/reports/` - Financial reports

## Email Configuration

The application is ready for SendGrid:

### For Development (Console Backend)

Email is printed to console by default. Set in `.env`:

```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### For Production (SendGrid)

1. Create SendGrid account and get API key
2. Update `.env`:

```
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

3. Install sendgrid backend:

```bash
pip install sendgrid-django
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Run tests with verbose output:

```bash
python manage.py test -v 2
```

Run specific test:

```bash
python manage.py test tests.TransactionTests.test_create_transaction
```

## Tests Included

- **Authentication**: Login requirement, user profile creation
- **Transactions**: Creation, validation, decimal precision
- **Categories**: Uniqueness constraints, user isolation
- **Budgets**: Overrun detection, percentage calculation
- **Decimal Handling**: Precision maintenance and aggregation
- **Views**: Access control and form submission

## Security Considerations

### Development

- `DEBUG=True` for development only
- Console email backend for testing

### Production

- Change `DJANGO_SECRET_KEY` to a strong random value
- Set `DEBUG=False`
- Set `SECURE_SSL_REDIRECT=True`
- Configure `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive data
- Enable CSRF and XFrame protection (already configured)
- Use PostgreSQL (never SQLite in production)
- Set up proper database backups

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn finance_tracker.wsgi --bind 0.0.0.0:8000
```

### Using Daphne (ASGI)

```bash
pip install daphne
daphne -b 0.0.0.0 -p 8000 finance_tracker.asgi:application
```

### Static Files

Collect static files for production:

```bash
python manage.py collectstatic
```

WhiteNoise is already configured to serve static files efficiently.

## Google OAuth Setup

1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials
3. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `https://yourdomain.com/accounts/google/login/callback/`
4. Get Client ID and Secret
5. Update `.env`:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_SECRET=your-secret
```

6. In Django admin, add Google OAuth provider details

## Troubleshooting

### PostgreSQL Connection Error

```
psycopg2.OperationalError: could not connect to server
```

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -l`

### Migration Error

```
django.db.utils.ProgrammingError: relation does not exist
```

Run migrations:

```bash
python manage.py migrate
```

### Module Not Found Error

Ensure virtual environment is activated and dependencies installed:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```


## Support

For issues or questions:

1. Check the troubleshooting section
2. Review Django documentation
3. Check django-allauth documentation for OAuth issues
4. Review test cases for usage examples
