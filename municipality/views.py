from django.shortcuts import render

# Create your views here.
def municipality(request):
    return render(request, 'municipality.html')