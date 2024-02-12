#AdminUsers authentication backend logic

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.backends import ModelBackend
from .models import AdminUser

class AdminUserAuthBackend(ModelBackend):
    """validates a AdminUser for login"""
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        """
        Validates a AdminUser using email or password.
       Returns the authenticated AdminUser object or None if authentication fails.
        """
        try:
            validate_email(username_or_email)
            is_valid_email_format = True
        except ValidationError:
            is_valid_email_format = False

        auth_type = 'email__iexact' if is_valid_email_format else 'username__iexact' # doing email__iexact=username_or_email will make it case insensitive but i think django handles that for us
        auth_param = {auth_type: username_or_email}

        try:
            admin_user = AdminUser.objects.get(**auth_param) # AdminUser.objects.get(email=username_or_email) [or username=username_or_email]
            if admin_user.check_password(password):
                return admin_user
        except AdminUser.DoesNotExist:
            pass

        return None
    
    def get_user(self, user_id):
        """
        Returns the AdminUser object using the given user_id.
        """
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None