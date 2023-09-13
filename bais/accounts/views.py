from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import CustomUser
from .forms import GreetingForm

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
    print("id: ", request.user.id)
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = GreetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user.app_greeting = form.cleaned_data['greeting']
            user.save()
            
            return HttpResponseRedirect("/accounts")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GreetingForm()

    return render(request, "accounts/greeting.html", {"form": form})