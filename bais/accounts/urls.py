from django.urls import path

from .views import Greeting, Goals, Colors, SignUpView
from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', TemplateView.as_view(template_name="accounts/index.html"), name='index'),
    path('greeting/', Greeting, name='greeting'),
    path('goals/', Goals, name='goals'),
    path('colors/', Colors, name='colors'),

]

'''
path('details', views.details, name='details'),
path('policies', views.policies, name='policies'),
'''