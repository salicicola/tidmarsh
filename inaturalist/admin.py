from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import *

class RecordAdmin3(admin.ModelAdmin):
    list_display = ('inat_id', 'created', 'saved_in', 'latname',  'revised_name', 'revised_by', 'revised_note', 'notes', ##'approved', 'comname', 'taxon_id'
                    'accuracy',) ##'latlon', 'accuracy', )  'observer',  'lcid', 'location', 'modified' 'latlon', 
    list_filter = ('category', 'lcid', 'revised_by', 'saved_in')
    search_fields = ('latname', 'comname', 'location', 'revised_name__latname', 'revised_name__pnid', 'inat_id') ## 'revised_name'
    raw_id_fields = ('revised_name',)
    readonly_fields = ['inat_id', ] ##'GUID',
    fieldsets = [
        (None,  {'fields': ['GUID',
'revised_name',
'revised_by',
('revised_note', 'saved_in', 'approved'),
('planted', 'urban'),
'notes', 
                            ('latname', 'comname', 'taxon_id'),
                            ('location', 'latlon', 'accuracy', ),
                            ('observer', 'verbose_date')] } 
        )]

admin.site.register(InatRecord, RecordAdmin3)
admin.site.register(ParsedLog)
