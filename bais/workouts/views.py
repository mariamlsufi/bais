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

    print(data)

    return render(request, "workouts/progress.html", {"exercises": data})

def Add(request):
    user = get_object_or_404(CustomUser, id=request.user.id)

    if request.method == "POST":

        workout = Workouts()
        workout.user = user
        workout.label = request.POST.get("workout_label", "")
        svgs = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="5vw" width="5vw" version="1.1" id="Capa_1" viewBox="0 0 721.285 721.285" xml:space="preserve"><g><g><path style="fill: var(--lightest)" d="M235.647,58.741l-46.446-45.08L202.861,0l46.446,45.08L235.647,58.741z M60.79,148.901    l46.446,45.081l13.661-13.661L74.451,135.24L60.79,148.901z M530.718,13.661L517.058,0L470.61,45.08l13.662,13.661L530.718,13.661    z M645.468,133.875l-45.08,46.446l13.66,13.661l46.447-45.081L645.468,133.875z M629.075,117.482l-17.758,16.393l-21.857-21.857    c4.098-9.563,2.732-20.491-5.465-28.688s-19.125-9.563-28.688-5.464l-27.322-28.688l19.125-19.125l-13.66-13.661l-46.445,45.081    l13.66,13.661l19.125-19.125l27.322,27.321l-92.895,94.259H265.701l-92.893-92.893l27.321-27.321L217.888,76.5l13.661-13.661    l-45.081-45.08L172.807,31.42l17.759,19.125l-27.321,27.321c-9.563-4.098-20.491-2.732-28.688,5.464    c-5.464,5.464-8.196,13.661-6.83,21.857c0,2.732,1.366,5.464,2.732,6.83l-21.857,21.857l-17.759-16.393l-13.661,13.661    l46.446,45.081l13.662-13.66l-20.491-20.491l20.491-20.492l144.803,148.902v416.652c0,19.125,15.027,34.151,34.152,34.151    s34.152-15.026,34.152-34.151V408.455h19.125v278.679c0,19.125,15.025,34.151,34.15,34.151s34.152-15.026,34.152-34.151V270.482    l146.17-148.902l20.49,20.491l-20.49,20.491l13.66,13.661l46.447-45.081L629.075,117.482z M359.959,159.83    c34.151,0,62.838-28.688,62.838-62.839s-28.688-62.839-62.838-62.839c-34.152,0-62.839,28.688-62.839,62.839    S325.808,159.83,359.959,159.83z"/></g></g></svg>', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="5vw" width="5vw" version="1.1" id="Capa_1" viewBox="0 0 50.463 50.463" xml:space="preserve"><g><g><path style="fill:var(--lightest);" d="M47.923,29.694c0.021-0.601-0.516-1.063-0.901-1.515c-0.676-2.733-2.016-5.864-3.961-8.971    C39.942,14.23,31.688,6.204,28.553,4.966c-0.158-0.062-0.299-0.097-0.429-0.126c-0.313-1.013-0.479-1.708-1.698-2.521    c-3.354-2.236-7.099-2.866-9.578-1.843c-2.481,1.023-3.859,6.687-1.19,8.625c2.546,1.857,7.583-1.888,9.195,0.509    c1.609,2.396,3.386,10.374,6.338,15.473c-0.746-0.102-1.514-0.156-2.307-0.156c-3.406,0-6.467,0.998-8.63,2.593    c-1.85-2.887-5.08-4.806-8.764-4.806c-3.82,0-7.141,2.064-8.95,5.13v22.619h4.879l1.042-1.849    c3.354-1.287,7.32-4.607,10.076-8.147C29.551,44.789,47.676,36.789,47.923,29.694z"/></g></g></svg>', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="var(--lightest)" height="5vw" width="5vw" version="1.1" id="Layer_1" viewBox="0 0 256 256" xml:space="preserve"><g><circle cx="127" cy="28.4" r="26.6"/><path d="M213.4,171.2h-49.8V97.3c0-1.8,1.5-3.3,3.3-3.3c0.6,0,1.2,0.2,1.7,0.5l30.1,17.3l-20.8,36c-3.2,5.6-1.3,12.7,4.3,15.9   c5.6,3.2,12.7,1.3,15.9-4.3l26.6-46c3.2-5.6,1.3-12.7-4.3-15.9l-51.6-29.8c-4.7-3.3-10-5.4-15.5-6L127,61.6h0h0l-26.3,0.1   c-5.5,0.6-10.8,2.7-15.5,6L33.6,97.5c-5.6,3.2-7.5,10.3-4.3,15.9l26.6,46c3.2,5.6,10.3,7.5,15.9,4.3c5.6-3.2,7.5-10.3,4.3-15.9   l-20.8-36l30.1-17.3c0.5-0.3,1.1-0.5,1.7-0.5c1.8,0,3.3,1.5,3.3,3.3v24.1v49.8H40.6c-9.2,0-16.6,7.4-16.6,16.6   c0,4.6,1.8,8.7,4.8,11.7l49.7,49.7c6.5,6.5,17,6.5,23.5,0c6.5-6.5,6.5-17,0-23.5l-21.3-21.3l46.2,0l0-13.3c0,0,0,0,0,0s0,0,0,0   l0,13.3l46.2,0l-21.3,21.3c-6.5,6.5-6.5,17,0,23.5c6.5,6.5,17,6.5,23.5,0l49.7-49.7c3-3,4.8-7.1,4.8-11.7   C230,178.7,222.6,171.2,213.4,171.2z"/></g></svg>']
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
        svgs = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="5vw" width="5vw" version="1.1" id="Capa_1" viewBox="0 0 721.285 721.285" xml:space="preserve"><g><g><path style="fill: var(--lightest)" d="M235.647,58.741l-46.446-45.08L202.861,0l46.446,45.08L235.647,58.741z M60.79,148.901    l46.446,45.081l13.661-13.661L74.451,135.24L60.79,148.901z M530.718,13.661L517.058,0L470.61,45.08l13.662,13.661L530.718,13.661    z M645.468,133.875l-45.08,46.446l13.66,13.661l46.447-45.081L645.468,133.875z M629.075,117.482l-17.758,16.393l-21.857-21.857    c4.098-9.563,2.732-20.491-5.465-28.688s-19.125-9.563-28.688-5.464l-27.322-28.688l19.125-19.125l-13.66-13.661l-46.445,45.081    l13.66,13.661l19.125-19.125l27.322,27.321l-92.895,94.259H265.701l-92.893-92.893l27.321-27.321L217.888,76.5l13.661-13.661    l-45.081-45.08L172.807,31.42l17.759,19.125l-27.321,27.321c-9.563-4.098-20.491-2.732-28.688,5.464    c-5.464,5.464-8.196,13.661-6.83,21.857c0,2.732,1.366,5.464,2.732,6.83l-21.857,21.857l-17.759-16.393l-13.661,13.661    l46.446,45.081l13.662-13.66l-20.491-20.491l20.491-20.492l144.803,148.902v416.652c0,19.125,15.027,34.151,34.152,34.151    s34.152-15.026,34.152-34.151V408.455h19.125v278.679c0,19.125,15.025,34.151,34.15,34.151s34.152-15.026,34.152-34.151V270.482    l146.17-148.902l20.49,20.491l-20.49,20.491l13.66,13.661l46.447-45.081L629.075,117.482z M359.959,159.83    c34.151,0,62.838-28.688,62.838-62.839s-28.688-62.839-62.838-62.839c-34.152,0-62.839,28.688-62.839,62.839    S325.808,159.83,359.959,159.83z"/></g></g></svg>', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="5vw" width="5vw" version="1.1" id="Capa_1" viewBox="0 0 50.463 50.463" xml:space="preserve"><g><g><path style="fill:var(--lightest);" d="M47.923,29.694c0.021-0.601-0.516-1.063-0.901-1.515c-0.676-2.733-2.016-5.864-3.961-8.971    C39.942,14.23,31.688,6.204,28.553,4.966c-0.158-0.062-0.299-0.097-0.429-0.126c-0.313-1.013-0.479-1.708-1.698-2.521    c-3.354-2.236-7.099-2.866-9.578-1.843c-2.481,1.023-3.859,6.687-1.19,8.625c2.546,1.857,7.583-1.888,9.195,0.509    c1.609,2.396,3.386,10.374,6.338,15.473c-0.746-0.102-1.514-0.156-2.307-0.156c-3.406,0-6.467,0.998-8.63,2.593    c-1.85-2.887-5.08-4.806-8.764-4.806c-3.82,0-7.141,2.064-8.95,5.13v22.619h4.879l1.042-1.849    c3.354-1.287,7.32-4.607,10.076-8.147C29.551,44.789,47.676,36.789,47.923,29.694z"/></g></g></svg>', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="var(--lightest)" height="5vw" width="5vw" version="1.1" id="Layer_1" viewBox="0 0 256 256" xml:space="preserve"><g><circle cx="127" cy="28.4" r="26.6"/><path d="M213.4,171.2h-49.8V97.3c0-1.8,1.5-3.3,3.3-3.3c0.6,0,1.2,0.2,1.7,0.5l30.1,17.3l-20.8,36c-3.2,5.6-1.3,12.7,4.3,15.9   c5.6,3.2,12.7,1.3,15.9-4.3l26.6-46c3.2-5.6,1.3-12.7-4.3-15.9l-51.6-29.8c-4.7-3.3-10-5.4-15.5-6L127,61.6h0h0l-26.3,0.1   c-5.5,0.6-10.8,2.7-15.5,6L33.6,97.5c-5.6,3.2-7.5,10.3-4.3,15.9l26.6,46c3.2,5.6,10.3,7.5,15.9,4.3c5.6-3.2,7.5-10.3,4.3-15.9   l-20.8-36l30.1-17.3c0.5-0.3,1.1-0.5,1.7-0.5c1.8,0,3.3,1.5,3.3,3.3v24.1v49.8H40.6c-9.2,0-16.6,7.4-16.6,16.6   c0,4.6,1.8,8.7,4.8,11.7l49.7,49.7c6.5,6.5,17,6.5,23.5,0c6.5-6.5,6.5-17,0-23.5l-21.3-21.3l46.2,0l0-13.3c0,0,0,0,0,0s0,0,0,0   l0,13.3l46.2,0l-21.3,21.3c-6.5,6.5-6.5,17,0,23.5c6.5,6.5,17,6.5,23.5,0l49.7-49.7c3-3,4.8-7.1,4.8-11.7   C230,178.7,222.6,171.2,213.4,171.2z"/></g></svg>']
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
            "num_sets" : sets.count()
        }
        exercise_info.append(dict)

    return render(request, "workouts/edit.html", {"workout": workout, "exercises":exercise_info})

