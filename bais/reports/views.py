from django.shortcuts import render

from .models import Report

# Create your views here.
def index(request):
    # View code here..
    reports = Report.objects.filter(user = request.user.id)
    return render(
        request,
        "reports/index.html",
        {
            "reports" : reports,
        }    
)