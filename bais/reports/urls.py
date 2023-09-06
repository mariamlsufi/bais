from django.urls import path
from django.views.generic.base import TemplateView
from .views import index


urlpatterns = [
    #send report data to function as well
    path('', index, name='index')
]

'''
path('<int:pk>',views.report, name='report'),
'''