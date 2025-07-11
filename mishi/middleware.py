from django.http import Http404
from django.shortcuts import render
from django.urls import resolve
from django.urls.exceptions import Resolver404

class Custom404Middleware:
    """
    Middleware personalizado para manejar URLs no encontradas
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Http404:
            # Redirigir a la página personalizada 404
            return render(request, '404.html', status=404)

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return render(request, '404.html', status=404)
        return None
