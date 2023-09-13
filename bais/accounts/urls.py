from django.urls import path

from .views import Greeting, SignUpView
from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', TemplateView.as_view(template_name="accounts/index.html"), name='index'),
    path('greeting/', Greeting, name='greeting'),

]

'''
path('colors', views.colors, name='colors'),
path('details', views.details, name='details'),
path('policoes', views.policies, name='policies'),
'''