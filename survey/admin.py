from django.contrib import admin
from .models import *

class GenericRecordAdmin(admin.ModelAdmin):
    list_display = ('GUID', "modified", 'plant', 'explicit_name', 'gps', 'gps_error',
                    'explicit_location', 'source') ## 'lcid', 'location', 
    search_fields = ('GUID', 'plant__pk', 'explicit_name', 'explicit_location')
    list_filter = ('source', )
    raw_id_fields = ('plant',)


admin.site.register(GenericRecord, GenericRecordAdmin)
