from django.contrib import admin

from .models import *

class Name4Admin(admin.ModelAdmin):
    list_display = ('pnid', 'level', 'latname', 'colnames', 'parent', 'upper', 'legacy_parent',
                    'rank', ) ## 'created', 'modified') ## 'authors', 'colnames', 
    search_fields = ('pnid', 'latname', 'parent__latname', 'sal_latname',
                     'legacy_parent__latname', 'colnames', 'note')
    list_filter = ('rank', 'category')
    raw_id_fields = ('parent', 'upper', 'legacy_parent')
##    exclude = ('legacy_parent', 'sal_latname', 'sal_authors', 'fid', 'disabled', 'longname', 'ccss') ## to be moved later
##    fields = ('category', ('rank', 'legacy'), 'level', 'latname', 'authors', 'colnames', 'parent', 'upper', 'note')
##    list_editable = ['latname', 'authors' ]
    fields = (('category', 'rank', 'level'), ('latname', 'sal_latname', ), ## 'ccss'
              ('authors', 'sal_authors', 'legacy',), ('parent', 'fid', 'disabled',), ('upper', 'legacy_parent'),
              'colnames', 'excluded',
              'note', 'caption',
              )
   ## list_editable = ('colnames',)
##
class PlantMetaAdmin(admin.ModelAdmin):
    list_display = ('spid', 'initial_name', 'introduced', 'invasive', 'invasive_mipag', ) ##  'rank', , 'updated' 'status', 'rare', 'introduced', 'invasive' 'counties'
    ## evergreen invasive updated status su_ba
    search_fields = ('spid', 'initial_name')
    list_filter = ('introduced', 'invasive', 'rare', )
    list_editable = ('invasive', 'invasive_mipag')

##
##class NameMiniAdmin(admin.ModelAdmin):
##    list_display = ( 'pnid', 'rank', 'upper', 'latname', 'authors', 'colnames', 'category')
##    fields = ('upper', ('latname', 'rank'), 'colnames','authors', 'note')
##    search_fields = ('latname', 'colnames', 'parent__latname', 'pnid')
##    list_filter = ('category', 'rank', )
##
class CommonNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ref_name', 'colname', 'created')
    search_fields = ('colname',)
##
##class LegacyNameAdmin(admin.ModelAdmin):
##    list_display = ('pnid', 'legacy_parent', 'sal_latname', 'sal_authors', 'longname', 
##                    'rank')
##    search_fields = ('sal_latname', 'pnid')
##    list_filter = ('rank', )
##    raw_id_fields = ('legacy_parent',)


##
##
admin.site.register(Name, Name4Admin) # 
admin.site.register(SpeciesMeta, PlantMetaAdmin)
admin.site.register(CommonName, CommonNameAdmin)
##admin.site.register(NameMini, NameMiniAdmin)
##admin.site.register(LegacyName, LegacyNameAdmin)
