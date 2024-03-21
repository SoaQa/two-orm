from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField()
    name = models.CharField(max_length=128, null=True, blank=True)


class UserAddresses(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)


class Address(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house_number = models.PositiveIntegerField()
    users = models.ManyToManyField(User, through="UserAddresses")


class Invoice(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
