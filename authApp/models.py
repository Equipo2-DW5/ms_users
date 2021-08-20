from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.fields import BooleanField

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, last_name, role, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(username=username, last_name=last_name, role=role, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, last_name, role, password):
        user = self.create_user(username=username, last_name=last_name, role=role, email=email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class labUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Name', max_length=15)
    last_name = models.CharField('LastName', max_length=15)
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Password', max_length=256)
    role = models.CharField('Rol', max_length=15)
    state = models.BooleanField('Estado', default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'last_name', 'role', 'password']

    def __str__(self):
        return '{"email": %s, "username": %s, "last_name": %s, "rol": %s}' %(self.email, self.username, self.last_name, self.role)