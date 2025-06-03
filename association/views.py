from django.shortcuts import render
from django.views import View
from .models import Association, Manager

# Create your views here.
def association(request):
    return render(request, 'association.html')

class Association(View):
    def get(self, request):
        associations = Association.objects.all()
        return render(request, 'association.html', {'association': associations})
        

