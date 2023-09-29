import datetime
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from accounts.models import CustomUser
from .models import Meals

# Create your views here.
def Index(request):
    return render(request, "food/index.html")

def FoodData(request, month, day, year): 
    user = get_object_or_404(CustomUser, id=request.user.id)

    meals = Meals.objects.filter(user=request.user.id, date_added__month = month, date_added__year = year, date_added__day = day)

    kcal = 0
    g_protein = 0
    veg = 0
    protein = 0
    grains = 0
    fruit = 0
    fats = 0
    dairy = 0
    photos = []
    meal_data = []

    for meal in meals:
        kcal += meal.kcal
        g_protein += meal.g_protein
        veg += meal.veg
        fruit += meal.fruit
        protein += meal.protein
        grains += meal.grains
        fats += meal.fats
        dairy += meal.dairy
        try:
            photos.append(meal.photo.url)
        except:
            pass
        meal_data += [meal.label, meal.kcal, meal.g_protein] 

    data = {
        'kcal': kcal,
        'g_protein': g_protein,
        'fruit': fruit,
        'veg': veg,
        'protein': protein,
        'grains': grains,
        'fats': fats,
        'dairy': dairy,
        'photos': photos,
        'meals': meal_data
    }
    return JsonResponse(data)