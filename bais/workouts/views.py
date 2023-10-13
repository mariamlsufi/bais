from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
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

def ProgressData(request):

    # get user and days
    user = get_object_or_404(CustomUser, id=request.user.id)
    days = request.GET.get('days', 0)

    progress_data = []

    for i in range(int(days)):
        curr_date = datetime.today() - timedelta(days=i)
        bests = Bests.objects.filter(user=user, date_added__year=curr_date.year, date_added__month=curr_date.month, date_added__day=curr_date.day)
        exercises_dict = {}

        for best in bests:
            exercises_dict[best.exercise.label] = best.reps * best.intensity
        
        progress_data.append(exercises_dict)

        
    # json response
    return JsonResponse({'data': progress_data})

def Progress(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    workouts = Workouts.objects.filter(user=user)
    data = []
    for workout in workouts:
        exercises = workout.rel_exercises.all()
        for exercise in exercises:
            data.append(exercise.label)

    print(data)

    return render(request, "workouts/progress.html", {"exercises": data})
