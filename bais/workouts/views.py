from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
from .models import Bests, Exercises, Sets, Workouts

# Create your views here.
def Workout(request, pk):
    user = get_object_or_404(CustomUser, id=request.user.id)
    workout = get_object_or_404(Workouts, pk=pk)
    exercises = workout.rel_exercises.all()

    if request.method == "POST":
        for exercise in exercises:
            best = Bests()
            best.workout = workout
            best.user = user
            best.exercise = exercise
            best.reps = request.POST.get(exercise.label + "_reps", 0)
            best.intensity = request.POST.get(exercise.label + "_intensity", 0)
            best.save()

        return HttpResponseRedirect("/workouts/")  
    
    if (workout.user != user):
        return HttpResponseRedirect("/workouts/")
    
    exercise_info = []
    for exercise in exercises:
        sets = Sets.objects.filter(workout = workout, exercise = exercise)
        set_info = []
        for set in sets:
            set_info.append({
                    "reps": set.reps,
                    "intensity": set.intensity
                })
        dict = {
            "label": exercise.label,
            "units": exercise.units,
            "sets": set_info,
        }
        exercise_info.append(dict)

    return render(request, "workouts/workout.html", {"workout": workout, "exercises":exercise_info})

def Index(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    workouts = Workouts.objects.filter(user=user)

    return render(request, "workouts/index.html", {"workouts": workouts})
    