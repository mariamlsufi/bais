from django.urls import path

from .views import SignUpView
from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', TemplateView.as_view(template_name="accounts/index.html"), name='index'),
]

'''
path('link-device', views.link, name='link-device'),
path('colors', views.colors, name='colors'),
path('details', views.details, name='details'),
path('polices', views.policies, name='policies'),
'''