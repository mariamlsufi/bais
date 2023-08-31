from django.urls import path

from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]

'''
path('', views.index, name='index'),
path('link-device', views.link, name='link-device'),
path('colors', views.colors, name='colors'),
path('details', views.details, name='details'),
path('polices', views.policies, name='policies'),
'''