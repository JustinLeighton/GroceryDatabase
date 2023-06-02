# inventory/admin.py

from django.contrib import admin
from .models import *

admin.site.register(UpcDetail)
admin.site.register(Scans)