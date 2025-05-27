from django.shortcuts import render

# Create your views here.
def veterinarian(request):
    return render(request, 'veterinarian.html')