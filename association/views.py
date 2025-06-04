from django.shortcuts import render, redirect
from django.views import View
from .models import Association, Manager
from .forms import AssociationForm

# Main association page
def association(request):
    associations = Association.objects.all()
    return render(request, 'association.html', {'associations': associations})


class AssociationListView(View):
    def get(self, request):
        associations = Association.objects.all()
        return render(request, 'association.html', {'associations': associations})

class AssociationCreateView(View):
    def get(self, request):
        form = AssociationForm()
        return render(request, 'asignar.html', {'form': form})

    def post(self, request):
        form = AssociationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('association')
        return render(request, 'asignar.html', {'form': form})