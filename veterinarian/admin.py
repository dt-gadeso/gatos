from django.contrib import admin
from .models import VetCenter, Agreement, VetService, Visit, VisitService

admin.site.register(VetCenter)
admin.site.register(Agreement)
admin.site.register(VetService)
admin.site.register(Visit)
admin.site.register(VisitService)
