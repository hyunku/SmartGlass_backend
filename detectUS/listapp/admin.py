from django.contrib import admin

# Register your models here.
from home.models import Building

from home.models import glass

from home.models import Company

from home.models import raw_data

from home.models import Issue

admin.site.register(Building)
admin.site.register(glass)
admin.site.register(Company)
admin.site.register(Issue)
admin.site.register(raw_data)


