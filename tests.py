from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from transactions.models import Transaction, Category
from budgets.models import Budget
from accounts.models import UserProfile


class UserAuthTests(TestCase):
    """Test authentication and login-required views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_required_for_dashboard(self):
        """Test that dashboard requires login."""
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access_dashboard(self):
        """Test that logged-in user can access dashboard."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_created_on_user_creation(self):
        """Test that UserProfile is created when User is created."""
        user = User.objects.create_user(username='newuser', password='pass')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())


class TransactionTests(TestCase):
    """Test transaction creation and validation."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Salary',
            type='income'
        )

    def test_create_transaction(self):
        """Test creating a transaction."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('5000.00'),
            date='2026-01-15',
            currency='INR'
        )
        self.assertEqual(transaction.amount, Decimal('5000.00'))
        self.assertEqual(transaction.user, self.user)

    def test_prevent_zero_amount_transaction(self):
        """Test that zero-amount transactions are prevented."""
        from django.core.exceptions import ValidationError

        transaction = Transaction(
            user=self.user,
            category=self.category,
            amount=Decimal('0.00'),
            date='2026-01-15'
        )
        with self.assertRaises(ValidationError):
            transaction.clean()

    def test_prevent_negative_amount_transaction(self):
        """Test that negative -amount transactions are prevented."""
        from django.core.exceptions import ValidationError

        transaction = Transaction(
            user=self.user,
            category=self.category,
            amount=Decimal('-100.00'),
            date='2026-01-15'
        )
        with self.assertRaises(ValidationError):
            transaction.clean()

    def test_category_deletion_preserves_transactions(self):
        """Test that deleting a category doesn't delete transactions."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            date='2026-01-15'
        )
        category_id = self.category.id

        # Delete category
        self.category.delete()

        # Transaction should still exist but category should be null
        transaction.refresh_from_db()
        self.assertIsNone(transaction.category)
        self.assertFalse(Category.objects.filter(id=category_id).exists())


class BudgetTests(TestCase):
    """Test budget creation and overrun detection."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.expense_category = Category.objects.create(
            user=self.user,
            name='Food',
            type='expense'
        )
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.expense_category,
            monthly_limit=Decimal('10000.00'),
            currency='INR'
        )

    def test_create_budget(self):
        """Test creating a budget."""
        self.assertEqual(self.budget.monthly_limit, Decimal('10000.00'))
        self.assertEqual(self.budget.user, self.user)

    def test_budget_not_exceeded(self):
        """Test budget status when not exceeded."""
        # Create transactions totaling 5000, which is less than 10000 limit
        from django.utils import timezone
        today = timezone.now().date()

        Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('5000.00'),
            date=today
        )

        spent = self.budget.get_spent_amount()
        self.assertEqual(spent, Decimal('5000.00'))
        self.assertFalse(self.budget.is_exceeded)

    def test_budget_exceeded(self):
        """Test budget overrun detection."""
        # Create transactions that exceed the budget
        from django.utils import timezone
        today = timezone.now().date()

        Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('6000.00'),
            date=today
        )
        Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('5000.00'),
            date=today
        )

        spent = self.budget.get_spent_amount()
        self.assertEqual(spent, Decimal('11000.00'))
        self.assertTrue(self.budget.is_exceeded)

    def test_budget_percentage_calculation(self):
        """Test budget percentage used calculation."""
        from django.utils import timezone
        today = timezone.now().date()

        Transaction.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('5000.00'),
            date=today
        )

        percentage = self.budget.get_percentage_used()
        # 5000 / 10000 * 100 = 50
        self.assertEqual(percentage, Decimal('50.00'))


class CategoryTests(TestCase):
    """Test category creation and constraints."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            user=self.user,
            name='Salary',
            type='income'
        )
        self.assertEqual(category.name, 'Salary')
        self.assertEqual(category.type, 'income')

    def test_unique_category_per_user_and_type(self):
        """Test that same category name can't exist twice for same user and type."""
        from django.db import IntegrityError

        Category.objects.create(
            user=self.user,
            name='Food',
            type='expense'
        )

        with self.assertRaises(IntegrityError):
            Category.objects.create(
                user=self.user,
                name='Food',
                type='expense'
            )

    def test_user_isolation(self):
        """Test that users have isolated categories."""
        user2 = User.objects.create_user(
            username='user2',
            password='pass'
        )

        cat1 = Category.objects.create(
            user=self.user,
            name='Food',
            type='expense'
        )
        cat2 = Category.objects.create(
            user=user2,
            name='Food',
            type='expense'
        )

        # Both should exist as they belong to different users
        self.assertNotEqual(cat1, cat2)
        self.assertEqual(Category.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Category.objects.filter(user=user2).count(), 1)


class ViewsTests(TestCase):
    """Test views for authentication and access control."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Salary',
            type='income'
        )

    def test_transaction_list_requires_login(self):
        """Test that transaction list requires login."""
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_transaction_create_view(self):
        """Test creating a transaction via POST."""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('transaction_create'), {
            'category': self.category.id,
            'amount': '5000.00',
            'date': '2026-01-15',
            'currency': 'INR',
            'description': 'Test transaction'
        })

        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)

        # Check that transaction was created
        self.assertTrue(Transaction.objects.filter(
            user=self.user,
            amount=Decimal('5000.00')
        ).exists())

    def test_budget_list_requires_login(self):
        """Test that budget list requires login."""
        response = self.client.get(reverse('budget_list'))
        self.assertEqual(response.status_code, 302)

    def test_category_list_requires_login(self):
        """Test that category list requires login."""
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)


class DecimalFieldTests(TestCase):
    """Test proper handling of Decimal fields for monetary calculations."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            user=self.user,
            name='Income',
            type='income'
        )

    def test_decimal_precision(self):
        """Test that Decimal precision is maintained."""
        amount = Decimal('1234.56')
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=amount,
            date='2026-01-15'
        )

        # Reload from database
        transaction.refresh_from_db()

        # Should maintain exact precision
        self.assertEqual(transaction.amount, Decimal('1234.56'))

    def test_decimal_aggregation(self):
        """Test that aggregation with Decimals works correctly."""
        from django.db.models import Sum

        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            date='2026-01-15'
        )
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('2000.50'),
            date='2026-01-20'
        )

        total = Transaction.objects.filter(user=self.user).aggregate(
            total=Sum('amount')
        )['total']

        # Should be 3000.50
        self.assertEqual(total, Decimal('3000.50'))
