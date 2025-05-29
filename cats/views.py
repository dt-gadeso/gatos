from django.shortcuts import render, redirect
from .form import CreateCat
from .models import Cat  # Importa tu modelo Cat
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
                print("Cleaned data:", form.cleaned_data)  # Debug: print cleaned_data to console
                cat = Cat(
                    catname=form.cleaned_data.get('catname'),
                    photo_file=form.cleaned_data.get('photo_file'),
                    chip=form.cleaned_data.get('chip'),
                    birthday=form.cleaned_data.get('birthday'),
                    sex=form.cleaned_data.get('sex'),
                    sterilized=form.cleaned_data.get('sterilized') == 'True',
                    dead=form.cleaned_data.get('dead') == 'True',
                    colony=form.cleaned_data.get('colony'),
                    user=request.user
                )
                cat.save()
                return redirect('cats')  
            except Exception as e:
                print("Error:", e)  # Debug: print error to console
                return render(request, 'formNewCat.html', { 
                    'form': form,
                    'error': f'Error al crear el gato: {str(e)}'
                })
        else:
            print("Form errors:", form.errors)  # Debug: print form errors to console
            return render(request, 'formNewCat.html', {
                'form': form,
                'error': 'Formulario inválido'
            })