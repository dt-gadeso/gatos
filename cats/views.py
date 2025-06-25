from django.shortcuts import render, redirect
from .form import CreateCat, EditCat
from .models import Cat
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse
from .models import Cat
from .form import EditCat
from colonies.models import Colony

@login_required
def cat(request):
    colonies = Colony.objects.all()  # Mostrar todas las colonias
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cat.html', {
        'colonies': colonies,
        'cats': cats
    })


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
                    colony=form.cleaned_data.get('colony'),
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
    filters = {}

    catname = request.GET.get('catname')
    colony_id = request.GET.get('colony')
    sex = request.GET.get('sex')
    sterilized = request.GET.get('sterilized')
    dead = request.GET.get('dead')

    if catname:
        filters['catname__icontains'] = catname
    if colony_id:
        filters['colony__id'] = colony_id
    if sex:
        filters['sex'] = sex
    if sterilized in ['true', 'false']:
        filters['sterilized'] = sterilized == 'true'
    if dead in ['true', 'false']:
        filters['dead'] = dead == 'true'

    cats = Cat.objects.filter(**filters)
    colonies = Colony.objects.all()

    context = {
        'cats': cats,
        'query': catname or '',
        'colony_id': colony_id or '',
        'sex': sex or '',
        'sterilized': sterilized or '',
        'dead': dead or '',
        'colonies': colonies
    }

    return render(request, 'cat_search_result.html', context)



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
        catname = self.request.GET.get('catname')
        if catname:
            queryset = queryset.filter(catname__icontains=catname)
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
