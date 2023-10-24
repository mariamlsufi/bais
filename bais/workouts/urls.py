from django.urls import path

from .views import Index, Progress, ProgressData, Workout, Add, Edit

urlpatterns = [
    path('<int:pk>/', Workout, name='workout'),
    path('', Index, name='workouts_index'),
    path('progress/data/', ProgressData, name='progress'),
    path('progress/', Progress, name='progress'),
    path('add/', Add, name="workout-add"),
    path('<int:pk>/edit/', Edit, name='edit'),
]
