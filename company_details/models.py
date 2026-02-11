from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    employee_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.username



class Employee(models.Model):
    emp_num = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_num


class Contact(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contacts')


class Payroll(models.Model):
    salary = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
