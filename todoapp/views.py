from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Notes, DarkMode
from .forms import UserForm
# Create your views here.

def loginPage(request):
    dark_mode = DarkMode.objects.get(id=1)
    page = True
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     pass
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password.')
    context = {'page': page,  'dark_mode': dark_mode.active}
    return render(request, 'todoapp/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    dark_mode = DarkMode.objects.get(id=1)
    page = False
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Your password must contain at least 8 characters.')
            messages.error(request, 'Your password can`t be entirely numeric.')

    context = {'forms':form, 'page': page, 'dark_mode': dark_mode.active}
    return render(request, 'todoapp/login_register.html', context)

def home(request):
    dark_mode = DarkMode.objects.get(id=1)
    q = request.GET.get('s_field') if request.GET.get('s_field') != None else ''
    user = request.user if request.user.is_authenticated else 0
    notes = Notes.objects.filter(
        Q(note__icontains = q) &
        Q(host = user)
    )
    context = {'notes':notes, 'dark_mode': dark_mode.active}
    return render(request, 'todoapp/home.html', context)

@login_required(login_url='login')
def click(request, pk):
    note = Notes.objects.get(id=pk)
    if note.active:
        note.active = False
    else:
        note.active = True
    note.save()
    return redirect('home')

def mode(request):
    dark_mode = DarkMode.objects.get(id=1)
    if dark_mode.active:
        dark_mode.active = False
    else:
        dark_mode.active = True
    dark_mode.save()
    return redirect('home')

@login_required(login_url='login')
def create(request):
    create = True
    dark_mode = DarkMode.objects.get(id=1)
    if request.method == 'POST':
        Notes.objects.create(
            host = request.user,
            note = request.POST.get('note'),
            active = False
        )
        return redirect('home')
    return render(request, 'todoapp/create.html', {'dark_mode': dark_mode.active, 'create':create})


@login_required(login_url='login')
def edit(request, pk):
    create = False
    dark_mode = DarkMode.objects.get(id=1)
    note = Notes.objects.get(id=pk)
    if request.method == 'POST':
        note.note = request.POST.get('note')
        note.save()
        return redirect('home')
    context = {'dark_mode': dark_mode.active, 'create': create, 'note': note}
    return render(request, 'todoapp/create.html', context)

@login_required(login_url='login')
def delete(request, pk):
    dark_mode = DarkMode.objects.get(id=1)
    note = Notes.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    context = {'note': note, 'dark_mode': dark_mode.active}
    return render(request, 'todoapp/delete.html', context)