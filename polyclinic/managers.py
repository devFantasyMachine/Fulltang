

from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password



class MedicalStaffManager(BaseUserManager):

    def _create_user(self, email, password, username, gender, cniNumber, role, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('MedicalStaff must have an email address')

        if not role:
            raise ValueError('MedicalStaff must have a role')

        if not cniNumber:
            raise ValueError('MedicalStaff must have a cniNumber')

        if not gender:
            raise ValueError('MedicalStaff must have a gender')

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        now = timezone.now()

        user = self.model(
            email=email,
            username=username,
            gender= gender ,
            cniNumber= cniNumber,
            role=role,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.password = make_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, **extra_fields)

