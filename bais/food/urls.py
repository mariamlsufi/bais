from django.urls import path
from .views import AddFood, Delete, Index, FoodData, AllFoods, EditMeal, Progress, ProgressData
urlpatterns = [
    path('', Index, name='food_index'),
    path("food-data/<month>/<day>/<year>/", FoodData, name="food_data"),
    path('add/', AddFood, name='food-add'),
    path('all/', AllFoods, name='allfood'),
    path('edit/<int:id>/', EditMeal, name='editmeal'),
    path('progress/data/', ProgressData, name="progress_data"),
    path('progress/', Progress, name='food-progress'),
    path('edit/<int:id>/delete/', Delete, name='delete'),

]