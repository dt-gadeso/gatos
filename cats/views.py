from django.shortcuts import render, redirect
from .form import CreateCat, EditCat
from .models import Cat
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse
from .models import Cat
from .form import EditCat

@login_required
def cat(request):
    return render(request, 'cat.html')

@login_required
def newCat(request):    
    if request.method == 'GET':
        return render(request, 'formNewCat.html', {
            'form': CreateCat(user=request.user)
        })
    else:
        form = CreateCat(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                # Usar ModelForm para guardar correctamente
                cat = Cat(
                    catname=form.cleaned_data.get('catname'),
                    photo_file=form.cleaned_data.get('photo_file'),
                    chip=form.cleaned_data.get('chip'),
                    birthday=form.cleaned_data.get('birthday'),
                    sex=form.cleaned_data.get('sex'),
                    sterilized=form.cleaned_data.get('sterilized') in [True, 'True', 'true', '1', 1],
                    dead=form.cleaned_data.get('dead') in [True, 'True', 'true', '1', 1],
                    colony=form.cleaned_data.get('colony'),  # Ya no puede ser None
                    user=request.user
                )
                cat.save()
                return redirect('cats')  
            except Exception as e:
                print("Error:", e)
                return render(request, 'formNewCat.html', { 
                    'form': form,
                    'error': f'Error al crear el gato: {str(e)}'
                })
        else:
            print("Form errors:", form.errors)
            return render(request, 'formNewCat.html', {
                'form': form,
                'error': 'Formulario inválido'
            })
        
@login_required
def searchEditCat(request):
    chip = request.GET.get('chip')
    try:
        cat = Cat.objects.get(chip=chip, user=request.user)
        return redirect('formEditCat', chip=cat.chip)
    except Cat.DoesNotExist:
        return render(request, 'cat.html', {
            'error': f'No se encontró un gato con el chip "{chip}".'
        })

@login_required
def editCat(request, chip):
    try:
        cat = Cat.objects.get(chip=chip, user=request.user)
    except Cat.DoesNotExist:
        return redirect('cats')

    if request.method == 'GET':
        form = EditCat(instance=cat, user=request.user)
        return render(request, 'formEditCat.html', {
            'form': form,
            'cat': cat,
            'chip': chip
        })
    else:
        form = EditCat(request.POST, request.FILES, instance=cat, user=request.user)
        if form.is_valid():
            try:
                form.save()
                return redirect('cats')
            except Exception as e:
                print("Error:", e)
                return render(request, 'formEditCat.html', {
                    'form': form,
                    'cat': cat,
                    'chip': chip,
                    'error': f'Error al editar el gato: {str(e)}'
                })
        else:
            print("Form errors:", form.errors)
            return render(request, 'formEditCat.html', {
                'form': form,
                'cat': cat,
                'chip': chip,
                'error': 'Formulario inválido'
            })

class CatListView(ListView):
    model = Cat
    template_name = 'cats/cat.html'
    context_object_name = 'cats'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(catname__icontains=q)
        return queryset

class CatUpdateView(UpdateView):
    model = Cat
    form_class = EditCat
    template_name = 'cats/formEditCat.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'success': True,
            'catname': self.object.catname,
            'chip': self.object.chip,
            'birthday': self.object.birthday.strftime('%Y-%m-%d'),
            'sex': self.object.sex,
            'sterilized': self.object.sterilized,
            'dead': self.object.dead,
            'colony': self.object.colony.id if self.object.colony else None,
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
