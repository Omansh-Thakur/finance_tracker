from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """Run initialization code when app is ready."""
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from accounts.models import UserProfile

        def create_user_profile(sender, instance, created, **kwargs):
            """Create a UserProfile when a User is created."""
            if created:
                UserProfile.objects.get_or_create(user=instance)

        post_save.connect(create_user_profile, sender=User)
