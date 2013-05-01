from weather.models import *
from django.contrib import admin

class report_admin(admin.ModelAdmin):
	search_fields = ('sol',)
	list_filter = ('terrestrial_date',)
admin.site.register(report,report_admin)

class magnitude_admin(admin.ModelAdmin):
	search_fields = ('sol',)
	list_filter = ('sol',)
admin.site.register(magnitude,magnitude_admin)