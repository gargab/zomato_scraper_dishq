from django.shortcuts import render
from models import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from serializers import *
from rest_framework.decorators import detail_route, list_route
from datetime import date as dt
from .zomato_scrape import *
# Create your views here.

class restaurantView(ModelViewSet):

	queryset=restaurant.objects.all()
	serializer_class=restaurantSerializer

	def get(self,request):
		query=restaurant.objects.all()
		serialized_query=restaurantSerializer(query,many=True)##Serialize the data to return as json
		return Response(serialized_query.data)

	#Serve data to front-end
	@list_route(methods=['get'])
	def get_all(self,request):
		query=restaurant.objects.values()
		restaurants=restaurantSerializer(query,many=True)##Serialize the data to return as json
		rests = restaurants.data
		for rest in rests:
			rev = review.objects.filter(rest_name=rest['name'])
			reviews = reviewSerializer(rev,many=True)
			rest['reviews'] = reviews.data

		return Response(restaurants.data)
