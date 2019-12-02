from django.contrib import admin

# Register your models here.
from demo_app.models import Publisher, Source, RevenueRecord

admin.site.register(Publisher)
admin.site.register(Source)
admin.site.register(RevenueRecord)