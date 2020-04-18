from django.contrib import admin
from .models import Table, TableRow, TableResult

# Register your models here.

admin.site.register(Table)
admin.site.register(TableRow)
admin.site.register(TableResult)