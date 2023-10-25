from time import localtime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
import csv
from accounts.models import CustomUser
from .models import CustomFood, Foods, Meals
from datetime import datetime, timedelta
from django.utils import timezone


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
        meal_data += [meal.label, meal.kcal, meal.g_protein, meal.pk] 

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

def AddFood(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        user = get_object_or_404(CustomUser, id=request.user.id)

        try: 
            meal = Meals(photo = request.FILES['file'])
            meal.user = user
            meal.kcal = request.POST.get("kcal", 0)
            meal.g_protein = request.POST.get("gprotein", 0)
            meal.label = request.POST.get("label", "")

            checkboxes = request.POST.getlist("checkboxes[]", {})
            meal.protein = "protein" in checkboxes
            meal.fruit = "fruit" in checkboxes
            meal.veg = "veg" in checkboxes
            meal.grains = "grains" in checkboxes
            meal.dairy = "dairy" in checkboxes
            meal.fats = "fats" in checkboxes

            if ("lookup_save" in checkboxes):
                food = CustomFood()
                food.user = user
                food.kcal = meal.kcal
                food.g_protein = meal.g_protein
                food.label = meal.label

                food.save()

            meal.date_added = request.POST.get("date")

            meal.save()
                
            return HttpResponseRedirect("/food/")
        except: 
            return render(request, "food/add.html", {"error": "please enter valid values in all fields"})
        
    return render(request, "food/add.html")

def AllFoods(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    input = request.GET.get('q', '')

    # "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=XxJnmRQsfKrvWwBz2tfrjbGZonJqau0Wv31NAaC7&query=" + input
    custom_foods = CustomFood.objects.filter(user=request.user.id, label__contains=input)
    foods = Foods.objects.filter(label__contains=input)
    food_list = []
    
    for food in custom_foods:
        food_list.append([food.label, food.kcal,food.g_protein])

    with open('food/foods.csv') as csv_file:
        print('reading')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0 and (input in row[0]):
                food_list.append(row)
            line_count+=1

    return JsonResponse({'custom_foods': food_list})

def EditMeal(request, id):


    meal = get_object_or_404(Meals, id=id, user=request.user.id)
    
    if request.method == "POST":
        try: 
            meal.kcal = request.POST.get("kcal", 0)
            meal.g_protein = request.POST.get("gprotein", 0)
            meal.label = request.POST.get("label", "")


            checkboxes = request.POST.getlist("checkboxes[]", {})
            print( checkboxes)
            meal.protein = "protein" in checkboxes
            meal.fruit = "fruit" in checkboxes
            meal.veg = "veg" in checkboxes
            meal.grains = "grains" in checkboxes
            meal.dairy = "dairy" in checkboxes
            meal.fats = "fats" in checkboxes

            meal.save()
        except: 
            render(request, "food/edit.html", {'meal': meal, 'error': "please enter valid values in all fields"})

        return HttpResponseRedirect("/food/")   


    return render(request, "food/edit.html", {'meal': meal})

def ProgressData(request):


    user = get_object_or_404(CustomUser, id=request.user.id)
    days = request.GET.get('days', 0)

    progress_data = []

    startdate = datetime.today()

    for i in range(int(days)):
        day_data = {
            "kcal" : 0,
            "g_protein" : 0,
            "fruit" : 0,
            "veg" : 0,
            "grains" : 0,
            "fats" : 0,
            "dairy" : 0,
            "protein" : 0,
        }
        # get meals for that day
        curr_date = datetime.today() - timedelta(days=i)
        meals = Meals.objects.filter(user=user, date_added__year=curr_date.year, 
                         date_added__month=curr_date.month, 
                         date_added__day=curr_date.day)
        # for each meal
        for meal in meals:
            day_data["kcal"] += meal.kcal
            day_data["g_protein"] += meal.g_protein
            day_data["fruit"] += meal.fruit
            day_data["veg"] += meal.veg
            day_data["grains"] += meal.grains
            day_data["fats"] += meal.fats
            day_data["dairy"] += meal.dairy
            day_data["protein"] += meal.protein

        progress_data.append(day_data)

    return JsonResponse({'data': progress_data})

def Progress(request):
    return render(request, "food/progress.html")