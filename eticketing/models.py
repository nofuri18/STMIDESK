
# models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Set default roles for superuser (admin)
        admin_role = Role.objects.get(id=5)  # Ganti ID yang sesuai dengan 'Admin' di Role model
        roles = [admin_role]
        
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        user.roles.set(roles)  # Gunakan set() untuk mengatur relasi many-to-many

        return user

# Tabel Role
class Role(models.Model):
    CUSTOMER = 1
    KASUBAG = 2
    KUNIT = 3
    TEKNISI = 4
    ADMIN = 5

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (KASUBAG, 'Kasubag'),
        (KUNIT, 'Kunit'),
        (TEKNISI, 'Teknisi'),
        (ADMIN, 'Admin'),
    ]

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role)

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        verbose_name=_('user permissions'),
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_roles_display(self):
        return ", ".join([role.get_id_display() for role in self.roles.all()])

    def __str__(self):
        return self.email
