from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class GreetingForm(forms.Form):
    greeting = forms.CharField(label="Greeting", max_length=100)

class GoalsForm(forms.Form):
    protein_goal = forms.DecimalField(label="protein")
    fruit_goal = forms.IntegerField(label="fruit")
    veg_goal = forms.IntegerField(label="veg")
    dairy_goal = forms.IntegerField(label="dairy")
    fats_goal = forms.IntegerField(label="fats")
    grains_goal = forms.IntegerField(label="grains")

    cal_goal = forms.IntegerField(label="cal")
    protein_goal_g = forms.IntegerField(label="protein_g")

class ColorsForms(forms.Form):
    lightest = forms.CharField(label="lightest")
    lighter = forms.CharField(label="lighter")
    darker = forms.CharField(label="darker")
    darkest = forms.CharField(label="darkest")

class ChangeDetails(forms.Form):
    password = forms.CharField()
    username = forms.CharField(label="username")
    email = forms.EmailField(label="email")