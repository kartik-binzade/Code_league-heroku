from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import login
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.raw_password = form.cleaned_data.get('password1')
            user.is_mentor = form.cleaned_data.get('is_mentor')
            user.level = form.cleaned_data.get('level')
            user.save()
            user = authenticate(username=user.username, password=user.raw_password)
            login(request, user)
            return redirect('myblogs:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect("myblogs:index")




