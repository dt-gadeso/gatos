from django.shortcuts import render, redirect
from .form import CreateCat, EditCat
from .models import Cat
from django.contrib.auth.decorators import login_required

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
                print("Cleaned data:", form.cleaned_data)
                cat = Cat(
                    catname=form.cleaned_data.get('catname'),
                    photo_file=form.cleaned_data.get('photo_file'),
                    chip=form.cleaned_data.get('chip'),
                    birthday=form.cleaned_data.get('birthday'),
                    sex=form.cleaned_data.get('sex'),
                    sterilized=form.cleaned_data.get('sterilized') == 'True',
                    dead=form.cleaned_data.get('dead') == 'True',
                    colony=form.cleaned_data.get('colony').id if form.cleaned_data.get('colony') else None,
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
def buscarEditarGato(request):
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