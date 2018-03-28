from django.shortcuts import render, get_object_or_404  # render page, return data or 404 page
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth

def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/') # !!!  Ошибка в этой строке
        else:
            login_error = "User not exist"
            context = {"login_error": login_error}
            return render(request, 'login_auth/login.html', context)
    else:
        return render(request, 'login_auth/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/') # !!!  Ошибка в этой строке
# модуль производит logout пользователя и перезапускает страницу
