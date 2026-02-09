# Getting Started - 5 Minute Setup

## Quick Start Guide

Follow these steps to get the Personal Finance Tracker running on your local machine.

### Prerequisites

- Python 3.8 or higher installed
- PostgreSQL 12 or higher installed and running
- pip and virtualenv
- A code editor (VS Code, PyCharm, etc.)

### Step-by-Step Setup

#### Step 1: Prepare the Project

```bash
cd c:\Project\FJassignment\code\finance_tracker
```

#### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Create PostgreSQL Database

**On Windows with PostgreSQL installed:**

```bash
# Open PostgreSQL prompt
psql -U postgres

# Create database
CREATE DATABASE finance_tracker;

# Exit
\q
```

**On Linux/macOS:**

```bash
sudo -u postgres psql

CREATE DATABASE finance_tracker;

\q
```

#### Step 5: Configure Environment

```bash
# Copy the template
cp .env.example .env

# Edit .env with your database credentials
# For local development, default values work:
# DB_NAME=finance_tracker
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=localhost
# DB_PORT=5432
```

#### Step 6: Run Migrations

```bash
python manage.py migrate
```

You should see output like:

```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ... (more migrations) ...
  Applying budgets.0001_initial... OK
```

#### Step 7: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:

```
Username: admin
Email: admin@example.com
Password: (enter a password)
```

#### Step 8: Start Development Server

```bash
python manage.py runserver
```

You should see:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

#### Step 9: Access the Application

Open your browser and visit:

- **Main app**: http://localhost:8000/
- **Admin panel**: http://localhost:8000/admin/

Login with your superuser credentials.

### Quick Test

1. **Create a Category**
   - Navigate to Transactions → Categories
   - Click "New Category"
   - Create "Salary" (Income type)
   - Create "Food" (Expense type)

2. **Create a Transaction**
   - Navigate to Transactions
   - Click "New Transaction"
   - Select "Salary" category, amount 50000, date today
   - Save

3. **View Dashboard**
   - Click "Dashboard"
   - See your total income displayed

4. **Create a Budget**
   - Navigate to Budgets
   - Click "New Budget"
   - Select "Food" category, monthly limit 5000
   - Save

### Common Issues & Solutions

**Issue**: `ModuleNotFoundError: No module named 'django'`

```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Then install again
pip install -r requirements.txt
```

**Issue**: `FATAL: database "finance_tracker" does not exist`

```bash
# Create the database (see Step 4 above)
# Then run migrations:
python manage.py migrate
```

**Issue**: `Error: [WinError 111] Connection refused`

```bash
# Make sure PostgreSQL is running
# On Windows: Services → Restart PostgreSQL service
# On Linux: sudo service postgresql restart
# On macOS: brew services restart postgresql
```

**Issue**: Port 8000 already in use

```bash
# Use a different port
python manage.py runserver 8001
# Visit http://localhost:8001/
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test -v 2

# Run specific test
python manage.py test tests.TransactionTests
```

### Next Steps

1. **Explore the Interface**
   - Dashboard shows financial overview
   - Create transactions
   - Set budgets
   - View reports

2. **Check the Admin Panel**
   - Visit http://localhost:8000/admin/
   - See all models
   - Create and edit records

3. **Read Documentation**
   - `README.md` - Complete guide
   - `QUICK_REFERENCE.md` - Common commands
   - `DEPLOYMENT.md` - Production setup

4. **Configure Email (Optional)**
   - Update `.env` with email settings
   - Default: console backend (emails print to console)
   - For production: Use SendGrid

5. **Git Setup (Optional)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Finance Tracker"
   ```

### Project Structure

```
finance_tracker/
├── manage.py                 # Django CLI
├── requirements.txt          # Dependencies
├── .env.example             # Config template
├── tests.py                 # All tests
├── finance_tracker/         # Main settings
│   ├── settings.py
│   └── urls.py
├── accounts/                # My Account
├── transactions/            # Income/Expenses
├── budgets/                 # Budget Limits
├── reports/                 # Analytics
└── templates/               # HTML Pages
    ├── accounts/
    ├── transactions/
    ├── budgets/
    └── reports/
```

### Key URLs

| URL                         | Purpose                       |
| --------------------------- | ----------------------------- |
| `/`                         | Home (redirects to dashboard) |
| `/dashboard/`               | Financial overview            |
| `/transactions/`            | View all transactions         |
| `/transactions/new/`        | New transaction               |
| `/transactions/categories/` | Manage categories             |
| `/budgets/`                 | View budgets                  |
| `/budgets/new/`             | New budget                    |
| `/reports/monthly/`         | Monthly report                |
| `/reports/categories/`      | Category report               |
| `/profile/`                 | User profile                  |
| `/accounts/logout/`         | Logout                        |
| `/admin/`                   | Admin panel                   |

### User Accounts

The app includes:

- **Registration** at `/accounts/signup/`
- **Login** at `/accounts/login/`
- **Google OAuth** (configured but optional)
- **Profile management**
- **All data is user-isolated** (secure!)

### Stopping the Server

Press `Ctrl+C` in the terminal running the server.

### Deactivating Virtual Environment

```bash
deactivate
```

### Next Time You Start

```bash
# Navigate to project
cd c:\Project\FJassignment\code\finance_tracker

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Start server
python manage.py runserver
```

## Troubleshooting Help

For detailed troubleshooting, see:

- [README.md](README.md) - Common issues section
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Troubleshooting guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Debug section

## Getting Help

1. Check the error message carefully
2. Search in README.md and QUICK_REFERENCE.md
3. Check Django logs: `python manage.py test -v 2`
4. Verify database connection: `psql -U postgres -c "SELECT 1"`

## Ready to Go? 🚀

You now have a fully functional Personal Finance Tracker!

**Key Features Available:**

- ✅ User registration & login
- ✅ Income/expense tracking
- ✅ Category management
- ✅ Monthly budgets
- ✅ Financial reports
- ✅ Email notifications
- ✅ Multi-currency support
- ✅ Receipt uploads

**Start creating transactions and managing your finances!**
