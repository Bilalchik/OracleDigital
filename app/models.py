from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Student(models.Model):
    full_name = models.CharField(max_length=225)
    mail = models.EmailField()
    date_of_birth = models.DateField()
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, related_name='students')
    address = models.CharField(max_length=123)
    gender = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Мужской'),
            (2, 'Женский'),
            (3, 'Другое'),
        )
    )
    image = models.ImageField(upload_to='media/images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Classroom(models.Model):
    title = models.CharField(max_length=223)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Teacher(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    moderate = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='teachers', null=True)
    item_name = models.CharField(max_length=223)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)


class School(models.Model):
    title = models.CharField(max_length=223)
    groups = models.ManyToManyField(Classroom, related_name='schools')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


