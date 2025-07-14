from django.shortcuts import render, redirect
from .form import CreateCat, EditCat, SearchCatForm
from .models import Cat
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.http import JsonResponse
from colonies.models import Colony
from django.db.models import Count, Q

@login_required
def cat(request):
    try:
        colonies = Colony.objects.all()
        cats = Cat.objects.filter(user=request.user)
        search_form = SearchCatForm()
    except Exception as e:
        print(f"Error in cat view: {e}")
        colonies = Colony.objects.none()
        cats = Cat.objects.none()
        search_form = SearchCatForm()
    
    return render(request, 'cat.html', {
        'colonies': colonies,
        'cats': cats,
        'search_form': search_form
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
                # Debug: ver los datos del formulario
                print("Form cleaned_data:", form.cleaned_data)
                
                cat = Cat(
                    catname=form.cleaned_data.get('catname'),
                    photo_file=form.cleaned_data.get('photo_file'),
                    chip=form.cleaned_data.get('chip'),
                    birthday=form.cleaned_data.get('birthday'),
                    sex=form.cleaned_data.get('sex'),
                    sterilized=form.cleaned_data.get('sterilized') == 'true',
                    dead=form.cleaned_data.get('dead') == 'true',
                    colony=form.cleaned_data.get('colony'),
                    user=request.user
                )
                
                # Debug: verificar los datos del gato antes de guardar
                print(f"Cat data before save: catname={cat.catname}, chip={cat.chip}, sterilized={cat.sterilized}, dead={cat.dead}")
                
                cat.save()
                
                # Debug: verificar que se guardó correctamente
                print(f"Cat saved successfully with ID: {cat.id}")
                
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
    filters = {'user': request.user}  # Filtrar por usuario actual
    
    # Crear formulario con datos GET
    search_form = SearchCatForm(request.GET)

    catname = request.GET.get('catname')
    colony_id = request.GET.get('colony')
    sex = request.GET.get('sex')
    sterilized = request.GET.get('sterilized')
    dead = request.GET.get('dead')

    # Aplicar filtros
    if catname and catname.strip():
        filters['catname__icontains'] = catname.strip()
    
    if colony_id and colony_id != '':
        try:
            filters['colony__id'] = int(colony_id)
        except ValueError:
            pass  # Ignorar valores inválidos
    
    if sex and sex != '':
        filters['sex'] = sex
    
    if sterilized in ['true', 'false']:
        filters['sterilized'] = sterilized == 'true'
    
    if dead in ['true', 'false']:
        filters['dead'] = dead == 'true'

    try:
        cats = Cat.objects.filter(**filters)
        colonies = Colony.objects.all()
    except Exception as e:
        print(f"Error in searchEditCat: {e}")
        cats = Cat.objects.none()
        colonies = Colony.objects.none()

    context = {
        'cats': cats,
        'query': catname or '',
        'colony_id': colony_id or '',
        'sex': sex or '',
        'sterilized': sterilized or '',
        'dead': dead or '',
        'colonies': colonies,
        'search_form': search_form
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

@login_required
def sterilized_counter(request):
    """Vista para mostrar contador de gatos esterilizados por colonia"""
    user = request.user
    
    # Verificar si el usuario es admin
    is_admin = user.is_superuser or (hasattr(user, 'role') and user.role and user.role.name == 'Admin')
    
    try:
        if is_admin:
            # Admin puede ver todas las colonias
            colonies = Colony.objects.all()
        else:
            # Usuario normal solo puede ver sus colonias
            colonies = Colony.objects.filter(user=user)
        
        colonies_data = []
        
        for colony in colonies:
            try:
                cats_data = Cat.objects.filter(colony=colony).aggregate(
                    total_male_sterilized=Count('id', filter=Q(sex='M', sterilized=True)),
                    total_female_sterilized=Count('id', filter=Q(sex='F', sterilized=True)),
                    total_male=Count('id', filter=Q(sex='M')),
                    total_female=Count('id', filter=Q(sex='F')),
                    total_sterilized=Count('id', filter=Q(sterilized=True)),
                    total_cats=Count('id')
                )
                
                colonies_data.append({
                    'colony': colony,
                    'male_sterilized': cats_data['total_male_sterilized'] or 0,
                    'female_sterilized': cats_data['total_female_sterilized'] or 0,
                    'total_male': cats_data['total_male'] or 0,
                    'total_female': cats_data['total_female'] or 0,
                    'total_sterilized': cats_data['total_sterilized'] or 0,
                    'total_cats': cats_data['total_cats'] or 0,
                })
            except Exception as e:
                print(f"Error processing colony {colony.id}: {e}")
                continue
    
    except Exception as e:
        print(f"Error in sterilized_counter: {e}")
        colonies_data = []
    
    context = {
        'colonies_data': colonies_data,
        'is_admin': is_admin,
        'user': user
    }
    
    return render(request, 'sterilized_counter.html', context)

@login_required
def test_search(request):
    """Vista simple para probar que el formulario funciona"""
    print("=== TEST SEARCH VIEW ===")
    print(f"Request method: {request.method}")
    print(f"Request GET: {request.GET}")
    print(f"Request POST: {request.POST}")
    
    # Mostrar todos los gatos del usuario
    cats = Cat.objects.filter(user=request.user)
    colonies = Colony.objects.all()
    
    return render(request, 'cat_search_result.html', {
        'cats': cats,
        'colonies': colonies,
        'query': 'TEST',
        'colony_id': '',
        'sex': '',
        'sterilized': '',
        'dead': '',
        'search_form': None
    })
