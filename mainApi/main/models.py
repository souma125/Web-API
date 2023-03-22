from django.db import models

# Create your models here.
class Address(models.Model):
    street_name = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    date_of_birth = models.DateField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

class Car(models.Model):
    model_name = models.CharField(max_length=100,choices=(('modelA','modelA'),('modelB','modelB')))
    manufacturing_date = models.DateTimeField(auto_now_add=True)
    manufacturer = models.CharField(max_length=100,choices=(('manufacturerA','manufacturerA'),('manufacturerB','manufacturerB')))
    color = models.CharField(max_length=100,choices=(('colorA','colorA'),('colorB','colorB')))

    # def __str__(self):
    #     return self.manufacturer
    # def __str__(self):
    #     return self.color
    
