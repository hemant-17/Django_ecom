from django.db import models

# Create your models here.
class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=400)
    pub_date=models.DateField()
    category=models.CharField(max_length=50 , default=" not present")
    sub_category=models.CharField(max_length=50 , default="notpresent")
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="shop/images" , default="not provided")

    def __str__(self):
        return self.product_name

class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=80 , default=" ")
    email=models.CharField(max_length=80 , default=" ")
    phone=models.CharField(max_length=80 , default=" ")
    desc=models.CharField(max_length=5000 , default=" ")





class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length =1000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=111)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
