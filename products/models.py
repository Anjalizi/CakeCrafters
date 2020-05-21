from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Product(models.Model):
	name = models.CharField(max_length=100)
	photo = models.ImageField(upload_to='./products/static/pictures/')
	cost = models.IntegerField()

	def __str__(self):
		return self.name

class ActiveCart(models.Model):
	order_id = models.AutoField(primary_key=True)
	item = models.ForeignKey(Product, on_delete=models.CASCADE)
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	order_date = models.DateTimeField(default=now)
	quantity = models.IntegerField(default=0)

	def __str__(self):
		return self.item.name;
