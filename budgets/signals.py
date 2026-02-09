from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from transactions.models import Transaction
from budgets.models import Budget


@receiver(post_save, sender=Transaction)
def check_budget_overrun(sender, instance, created, **kwargs):
    """
    Signal handler to check if a transaction causes budget overrun.
    Sends email notification if budget is exceeded.
    """
    if not created:
        return  # Only check on creation, not update

    try:
        # Check if category exists and is an expense
        if not instance.category or instance.category.type != 'expense':
            return

        # Get the budget for this category
        try:
            budget = Budget.objects.get(category=instance.category)
        except Budget.DoesNotExist:
            return

        # Check if budget exceeded
        if budget.is_exceeded:
            send_budget_overrun_email(instance.user, budget, instance)

    except Exception as e:
        # Log error but don't fail the transaction
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error checking budget overrun: {str(e)}")


def send_budget_overrun_email(user, budget, transaction):
    """Send email notification for budget overrun."""
    try:
        subject = f"Budget Alert: {budget.category.name} Exceeded"
        context = {
            'user': user,
            'budget': budget,
            'transaction': transaction,
            'spent': budget.get_spent_amount(),
        }

        html_message = render_to_string('budgets/budget_overrun_email.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending budget overrun email: {str(e)}")
