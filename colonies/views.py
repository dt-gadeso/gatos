from django.shortcuts import render

# Create your views here.
def colonies(request):
    return render(request, 'colonies.html')
