from django.shortcuts import render, redirect
from TravelBuddyApp.models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        safe_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name=name, username=username, password=safe_password.decode())
        request.session['userid'] = user.id
        return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        username = request.POST['username']
        user = User.objects.get(username=username)
        request.session['userid'] = user.id
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    user = User.objects.get(id=request.session['userid'])
    destinations = Destination.objects.all()
    context = {
        'user': user,
        'destinations': destinations
    }
    return render(request, 'travels.html', context)

def addpage(request):
    return render(request, 'addpage.html')

def add(request):
    errors = Destination.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        user = User.objects.get(id=request.session['userid'])
        destination = request.POST['destination']
        description = request.POST['description']
        traveldatefrom = request.POST['traveldatefrom']
        traveldateto = request.POST['traveldateto']
        newdestination = Destination.objects.create(destination=destination, description=description, traveldatefrom=traveldatefrom, traveldateto=traveldateto)
        newdestination.users.add(user)
        return redirect('/travels')

def showdestination(request, id):
    destination = Destination.objects.get(id=id)
    context = {
        'destination': destination
    }
    return render(request, 'showdestination.html', context)

def jointravelplan(request, id):
    user = User.objects.get(id=request.session['userid'])
    destination = Destination.objects.get(id=id)
    destination.users.add(user)
    return redirect('/travels')
