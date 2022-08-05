from django.contrib import admin

# Register your models here.
from home.models import Building

from home.models import Glass

from home.models import Company

from home.models import Raw_data

from home.models import Issue

admin.site.register(Building)
admin.site.register(Glass)
admin.site.register(Company)
admin.site.register(Issue)
admin.site.register(Raw_data)


