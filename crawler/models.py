from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProductInfo(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    img   = models.ImageField(upload_to="pics",max_length=255)
    ratings = models.FloatField()
    search_item  = models.CharField(max_length=255)
class product_user_compare(models.Model):
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
