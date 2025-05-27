from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.
def users(request):
    return render(request, 'signup.html', {'form': UserCreationForm()})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
            
