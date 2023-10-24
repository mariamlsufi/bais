from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import CustomUser
from .forms import ChangeDetails, ColorsForms, GoalsForm, GreetingForm

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def Greeting(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(CustomUser, id=request.user.id)

    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GreetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user.app_greeting = form.cleaned_data['greeting']
            user.save()
            
            return HttpResponseRedirect("/accounts/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GreetingForm()

    return render(request, "accounts/greeting.html", {"form": form})

def Goals(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(CustomUser, id=request.user.id)
    print("id: ", request.user.id)
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GoalsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user.protein_goal = form.cleaned_data['protein_goal']
            user.fruit_goal = form.cleaned_data['fruit_goal']
            user.veg_goal = form.cleaned_data['veg_goal']
            user.dairy_goal = form.cleaned_data['dairy_goal']
            user.fats_goal = form.cleaned_data['fats_goal']
            user.grains_goal = form.cleaned_data['grains_goal']
            user.cal_goal = form.cleaned_data['cal_goal']
            
            user.save()
            
            return HttpResponseRedirect("/accounts/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GoalsForm()

    return render(request, "accounts/goals.html", {"form": form})


def Colors(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(CustomUser, id=request.user.id)
    print("id: ", request.user.id)
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ColorsForms(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user.lightest = form.cleaned_data['lightest']
            user.lighter = form.cleaned_data['lighter']
            user.darker = form.cleaned_data['darker']
            user.darkest = form.cleaned_data['darkest']

            user.save()
            
            return HttpResponseRedirect("/accounts/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ColorsForms()

    return render(request, "accounts/colors.html")

def Details(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(CustomUser, id=request.user.id)
    print("id: ", request.user.id)
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ChangeDetails(request.POST)
        # check whether it's valid:
        error = ""
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            if (form.cleaned_data['password']):
                user.set_password(form.cleaned_data['password'])

            try:
                user.save()
            except IntegrityError:
                error = "please try a different username"
                return render(request, "accounts/login-details.html", {"error": error})
            
            return HttpResponseRedirect("/accounts/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangeDetails()

    return render(request, "accounts/login-details.html")