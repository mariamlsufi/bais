from datetime import date, timedelta
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
from food.models import Meals
from workouts.models import Bests, Exercises, Workouts

from .models import Report

# Create your views here.
def index(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    reports = []

    start_date = user.date_created
    while (start_date <= date.today()):
        report = {
            "start_date": start_date,
            "end_date": start_date + timedelta(7),
            "cal_in":0,
            "g_protein":0,
            "fruit":0,
            "veg":0,
            "dairy":0,
            "fats":0,
            "protein":0,
            "grains":0,
        }

        #avg lift improvement
        bests = Bests.objects.filter(user=user, date_added__range=[report["start_date"], report["end_date"]])
        workouts = Workouts.objects.filter(user=user)
        percent_improvement = 0
        num_exercises = 0
        for workout in workouts:
            exercises = workout.rel_exercises.all()
            num_exercises += len(exercises)
            for exercise in exercises:
                exercise_bests = bests.filter(exercise = exercise)
                max = 0
                min = 10000000
                for best in exercise_bests:
                    value = best.reps * best.intensity
                    if value >= max:
                        max = value
                    if value <= min:
                        min = value
                percent_improvement += (max-min)/max
        if (num_exercises != 0): 
            percent_improvement = percent_improvement/num_exercises * 100
        else:
            percent_improvement = "~"

        report["percent_improvement"] = percent_improvement
        
        # num workouts completed
        report["num_workouts"] = Workouts.objects.filter(user=user, date_used__range=[report["start_date"], report["end_date"]]).count()

        meals = Meals.objects.filter(user=user, date_added__range=[report["start_date"], report["end_date"]])
        # cals in; avg cals im
        
        for meal in meals:
            report["cal_in"] += meal.kcal
            report["g_protein"] += meal.g_protein

            report["fruit"] += meal.fruit
            report["veg"] += meal.veg
            report["dairy"] += meal.dairy
            report["fats"] += meal.fats
            report["protein"] += meal.protein
            report["grains"] += meal.grains

        reports.append(report)
        start_date = start_date + timedelta(8)

    return render(request, "reports/index.html", { 
        "reports" : reports, 
        "protein_goal": user.protein_goal * 7,
        "grains_goal": user.grains_goal * 7,
        "fats_goal": user.fats_goal * 7,
        "veg_goal": user.veg_goal * 7,
        "fruit_goal": user.fruit_goal * 7,
        "dairy_goal": user.dairy_goal * 7

        }    
)