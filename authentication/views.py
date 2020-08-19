from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='signin')
def home(request):
    # return render(request, 'HOME.html')
    return render(request, 'MENU_OPCIONES/LAYOUT.html')


@login_required(login_url='signin')
def home_bad(request):
    return render(request, 'HOME.html')
