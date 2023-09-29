from django.urls import path
from .views import Index, FoodData
urlpatterns = [
    path('', Index, name='index'),
    path("food-data/<month>/<day>/<year>/", FoodData, name="food_data")

]

'''
path('add', views.add, name='add'),
path('progress', views.progress, name='progress'),
path('<int:pk>', views.food, name='food'),
'''