from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
from .models import Bests, Exercises, Sets, Workouts

# Create your views here.
def Workout(request, pk):
    if (request.user.is_authenticated):
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

                workout.date_used = datetime.today()
                workout.save()

            return HttpResponseRedirect("/workouts/" + str(pk) + "/edit/")
        
        if (workout.user != user):
            return HttpResponseRedirect("/workouts/")
        
        exercise_info = []
        num_sets = []
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
            num_sets.append(len(sets))

    return render(request, "workouts/workout.html", {"workout": workout, "exercises":exercise_info, "num_sets": num_sets})

def Index(request):
    if (request.user.is_authenticated):
        user = get_object_or_404(CustomUser, id=request.user.id)
        workouts = Workouts.objects.filter(user=user)

        return render(request, "workouts/index.html", {"workouts": workouts})
    return render(request, "workouts/index.html")

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

    return render(request, "workouts/progress.html", {"exercises": data})

def Add(request):
    user = get_object_or_404(CustomUser, id=request.user.id)

    if request.method == "POST":

        workout = Workouts()
        workout.user = user
        workout.label = request.POST.get("workout_label", "")

        svgs = open("workouts\svgs.csv").readlines()        
        workout.svg = svgs[int(request.POST.get("icon"))]

        workout.save()
        
        exercise_names = request.POST._getlist("exercise_name")
        exercise_sets = request.POST._getlist("num_sets")
        exercise_units = request.POST._getlist("units")
        set_reps = request.POST._getlist("set_reps")
        set_intensities = request.POST._getlist("set_intensity")
        

        added = 1
        for i in range(1, len(exercise_names)):
            exercise = Exercises()
            exercise.label = exercise_names[i]
            exercise.units = exercise_units[i]
            exercise.save()
            for j in range(int(exercise_sets[i])):
                set = Sets()
                set.workout = workout
                set.exercise = exercise
                set.reps = set_reps[added + j]
                set.intensity = set_intensities[added + j]

                set.save()

            added += int(exercise_sets[i])

            workout.rel_exercises.add(exercise)

            exercise.save()

        workout.save()

        return HttpResponseRedirect("/workouts/")

    return render(request, "workouts/add.html")

def Edit(request, pk):
    user = get_object_or_404(CustomUser, id=request.user.id)
    workout = get_object_or_404(Workouts, pk=pk)
    exercises = workout.rel_exercises.all()

    if request.method == "POST":
       
        workout.user = user
        workout.label = request.POST.get("workout_label", "")
        svgs = open("workouts\svgs.csv").readlines()        
        workout.svg = svgs[int(request.POST.get("icon"))]

        workout.save()

        exercise_names = request.POST._getlist("exercise_name")
        exercise_sets = request.POST._getlist("num_sets")
        exercise_units = request.POST._getlist("units")
        exercise_ids = request.POST._getlist("id")
        set_reps = request.POST._getlist("set_reps")
        set_intensities = request.POST._getlist("set_intensity")
        

        # for each exercise
        set_num = 1
        for i in range(1, len(exercise_names)):
            exercise = Exercises()
            if (i - 1 < len(exercise_ids)):
                exercise = Exercises.objects.get(id = exercise_ids[i - 1])
            exercise.units = exercise_units[i]
            exercise.label = exercise_names[i]
            
            exercise.save()
            # add new sets
            if (exercise_sets[i] != '~'):
                # delete old sets
                prev_sets = Sets.objects.filter(exercise=exercise)
                for set in prev_sets:
                    set.delete()

                for j in range(int(exercise_sets[i])):
                    set = Sets()
                    set.reps = set_reps[set_num]
                    set.intensity = set_intensities[set_num]
                    set.workout = workout
                    set.exercise = exercise
                    set.save()
                    set_num += 1

            workout.rel_exercises.add(exercise)
            exercise.save()


        return HttpResponseRedirect("/workouts/")
    
    num_sets = []
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
            "pk": exercise.pk,
            "sets": set_info,
        }
        exercise_info.append(dict)
        num_sets.append(len(sets))

    return render(request, "workouts/edit.html", {"workout": workout, "exercises":exercise_info, "num_sets":num_sets})

def Delete(request, pk):
    if (request.user.is_authenticated):
        user = get_object_or_404(CustomUser, id=request.user.id)
        workout = get_object_or_404(Workouts, pk=pk)
    
        if (workout.user == user):
            workout.delete()

    return HttpResponseRedirect("/workouts/")

def DeleteExercise(request, pk, id):
    if (request.user.is_authenticated):
        user = get_object_or_404(CustomUser, id=request.user.id)
        exercise = get_object_or_404(Exercises, pk=id)

        exercise.delete()

    return HttpResponseRedirect("/workouts/")