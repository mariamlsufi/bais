from django.urls import path

from .views import Workout

urlpatterns = [
    path('<int:pk>/', Workout, name='workout'),
]

'''
path('', views.index, name='index'),
path('add', views.add, name='add'),
path('progress', views.progress, name='progress'),
path('<int:pk>/edit', views.edit, name='edit'),
'''