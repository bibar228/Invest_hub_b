from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, phone):
        if not email:
            raise ValueError("Вы не ввели Email")

        if not phone:
            raise ValueError("Вы не ввели Phone number")

        user = self.model(email=email, password=password, phone=phone)

        user.set_password(password)

        user.save(using=self._db)
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, password, phone):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, password, phone)

    def create_superuser(self, email, password, phone):
        user = self.create_user(email, password, phone)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Создаём класс User
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(max_length=50, unique=True, blank=False)
    phoneNumberRegex = RegexValidator(regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=12, unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'