from django.shortcuts import render

# Create your views here.
def Hello(request):
    return render(request, 'index.html')

def custom_404(request, exception=None):
    """Vista personalizada para manejar errores 404"""
    return render(request, '404.html', status=404)
