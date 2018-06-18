from rest_framework import routers
from zomato_scrapers.views import restaurantView as ZomatoView




router = routers.SimpleRouter()

router.register(r'zomato',ZomatoView)
