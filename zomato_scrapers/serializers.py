from rest_framework import serializers
from models import *


class restaurantSerializer(serializers.ModelSerializer):
	class Meta:
		model=restaurant
		fields='__all__'

class reviewSerializer(serializers.ModelSerializer):
	class Meta:
		model=review
		fields='__all__'
