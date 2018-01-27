# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.messages import error

def index(request):
    return render(request, 'buddy/index.html')

def register(request):
    valid= User.objects.validate_reg(request.POST)
    if type(valid) == list:
        for e in valid:
            messages.error(request, e)
        return redirect('/')
    request.session['user_id'] = valid.id
    return redirect ('/success')

def login(request):
    valid = User.objects.validate_login(request.POST)
    if type(valid) == list:
        for e in valid:
            messages.error(request, e)
        return redirect('/')
    request.session['user_id'] = valid.id
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError: 
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']) #getting id from db and using it to display user info and other actions depending on app built
    }
    return render(request, 'buddy/success.html', context)

def logout(request):
    request.session.clear()
    return render(request,'buddy/index.html')


def travels(request):
	if 'user_id' in request.session:
		current_user = User.objects.get(id=request.session['user_id'])
		my_trips = current_user.travelers.all()
		travels = Travel.objects.exclude(id__in=my_trips).order_by('-created_at')

		context = {
			'current_user': current_user,
			'travels': travels,
			'my_trips': my_trips,
		}

		return render(request, "buddy/travels.html", context)

	return redirect('/')


def add_trip(request):
	if request.method == "POST":
		errors = Travel.objects.validate_travel(request.POST)
		current_user = User.objects.get(id=request.session['user_id'])

		if not errors:
			travel = Travel.objects.createTravel(request.POST, current_user)			
			request.session['travel_id'] = travel.id
			return redirect('/travels')
		if type(errors) == list:
			for e in errors:
				messages.error(request, e)
			return redirect('/add_plan')
	
	return redirect("/add_plan")

def add_plan(request):
	return render(request, "buddy/add.html")

def destination(request, id):
	travel = Travel.objects.get(id=id)
	current_user = User.objects.get(id=request.session['user_id'])
	travelers = travel.joined_by.all()
	context = {
		'current_user': current_user,
		'travel': travel,
		'travelers': travelers,
	}
	return render(request, "buddy/destination.html", context)

def travelers(request, id):
	if request.method == "POST":
		if 'user_id' in request.session:
			current_user = User.objects.get(id=request.session['user_id'])
			joined_by = Travel.objects.get(id=id)
			current_user.travelers.add(joined_by)

			return redirect('/travels')
