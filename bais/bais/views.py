from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
from food.models import Meals
from reports.models import Report
from workouts.models import Workouts

def Index(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)
        workouts = Workouts.objects.filter(user=user).order_by('date_used')[:3]
        if Report.objects.filter(user=user):
            report = Report.objects.filter(user=user)[0]
        else:
            report = 0

        meals = Meals.objects.filter(user=user, date_added__month = datetime.today().month, date_added__year = datetime.today().year, date_added__day = datetime.today().day)
        cal_in = 0
        g_protein = 0
        for meal in meals:
            cal_in += meal.kcal
            g_protein += meal.g_protein

        return render(request, "home.html", {"workouts": workouts, "greeting":user.app_greeting, "report": report, "g_protein": g_protein, "cal_in": cal_in})
    
    return render(request, "home.html")