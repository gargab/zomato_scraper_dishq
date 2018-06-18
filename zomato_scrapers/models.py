from __future__ import unicode_literals

from django.db import models

# Create your models here.
"""
class item(models.Model):
	item_no=models.IntegerField(default=10)
	item_name=models.CharField(max_length=1000)

#	def __str__ defines what happens when the object is cast as a string
#	This is used to display representative value while viewing the objects on admin page

	def __str__(self):
		return self.item_name

"""

class restaurant(models.Model):
	name=models.CharField(max_length=1000)
	lat=models.CharField(max_length=1000)
	long=models.CharField(max_length=1000)
	url=models.CharField(max_length=1000)
	rating=models.CharField(max_length=1000,blank=True,null=True)
	address=models.CharField(max_length=1000,blank=True,null=True)
	def __str__(self):
		return str(self.url) + " " + str(self.address)

class review(models.Model):
	rest_name=models.CharField(max_length=1000)
	cust_name=models.CharField(max_length=1000)
	content=models.CharField(max_length=90000)
	def __str__(self):
		return str(self.cust_name) + " " + str(self.content)
