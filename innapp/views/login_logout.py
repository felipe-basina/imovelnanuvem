# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth


def logout_user(request):
    auth.logout(request)
    return render(request, 'innapp/login.html', {'message': 'Você saiu do sistema!', 'status': 'success'})


def login_user(request):
    logout(request)
    context = {}
    if request.POST:
        context = {'message': 'usuário/senha inválidos', 'status': 'danger'}
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

    return render(request, 'innapp/login.html', context)