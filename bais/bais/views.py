from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
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
        

        return render(request, "home.html", {"workouts": workouts, "greeting":user.app_greeting, "report": report})
    
    return render(request, "home.html")