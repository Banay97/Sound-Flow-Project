from django.contrib import admin
from .models import User, Session

# Register your models here.

admin.site.register(User)
admin.site.register(Session)