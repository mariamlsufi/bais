from django.urls import path

from .views import Index, Progress, ProgressData, Workout

urlpatterns = [
    path('<int:pk>/', Workout, name='workout'),
    path('', Index, name='index'),
    path('progress/data/', ProgressData, name='progress'),
    path('progress/', Progress, name='progress'),
]

'''
path('add', views.add, name='add'),
path('<int:pk>/edit', views.edit, name='edit'),
'''