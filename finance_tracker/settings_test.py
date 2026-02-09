"""
Django settings for testing with SQLite instead of PostgreSQL.
"""

from finance_tracker.settings import *  # noqa

# Override database to use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use in-memory database for faster tests
    }
}

# Disable migrations for faster tests if needed
# This is useful for schema testing
