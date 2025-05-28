from django.contrib import admin
from .models import User, Role, Member, Observation

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Member)
admin.site.register(Observation)
