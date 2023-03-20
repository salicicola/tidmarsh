from django.contrib import admin
from .models import *

class GalleryPlantPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'imid', 'genname', 'latname', 'authors', 'fid', 'spid', 'nr',  'locality')
                    ##'plant',) 'locality',
 ##                     'is_planted', 'is_verified', 'modified')
                    ##'phid', 'town', 
                    ##'lcid', 'inid', 'location', 'date', 'caption', 'modified') 
    search_fields = ('town',  'imid', 'phid', ) ## removed not searceable attributes 'spid', 'fid' etc
    list_filter = ('is_planted', 'is_verified')
    raw_id_fields = ('plant', 'locality')

class AnimalPhotoAdmin(admin.ModelAdmin):
    list_display = ('imid', 'genname', 'latname', 'authors', 'fid', 'spid', 'nr', )
    search_fields = ('town', 'imid', 'phid', ) ## 'gid', 'genname',  'latname', 'spid', 'fid'
##    list_filter = ('famname',) ## this is an attribute

class NameDeletedAdmin(admin.ModelAdmin):
    list_display = ( 'imid', 'spid', 'genname', 'latname', 'reason', 'uid')
    fields = ('imid', ('spid', 'genname', 'latname'),
              ('location', 'lcid',), 'reason', 'uid')
    ##search_fields = ('latname', 'colnames', 'parent__latname', 'pnid')
    ##list_filter = ('category', 'rank', )

class FileAdmin(admin.ModelAdmin):
    list_display = ('PID', 'imid', 'committed', 'tables', 'size', 'modified', 'md5') ## 'abspath'
    search_fields = ('imid',)
    list_filter = ('committed', 'year', 'tables') ## status always tomcat here 

class NameIndexAdmin(admin.ModelAdmin):
    list_display = ("id", "spid", "name", "long_name", "classification", "category",
                    "images", "pubimages", "status", "created")
    search_fields = ('name', 'long_name')
    list_filter = ("classification", "category")

class TidmarshRecordAdmin(admin.ModelAdmin):
    list_display = ("id", 'plantname',"plant_id", "photo_url", "coordinates", 
                    "lat", "lon", "lcid", "uid", "actual_uid", "observed", "notes", "created",)
    list_filter = ("uid", "plantname",)

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ("pk", 'plant',"note", "comments")
    ##list_filter = ("uid", "plantname",)
    raw_id_fields = ('plant', )

class ImagesLog(admin.ModelAdmin):
    list_display = ("imid", 'plant',"status", "published")
    list_filter = ("status", )





admin.site.register(VascularImage, GalleryPlantPhotoAdmin)
admin.site.register(NonVascularImage, GalleryPlantPhotoAdmin)
admin.site.register(AnimalImage, AnimalPhotoAdmin)
admin.site.register(VariaImage, GalleryPlantPhotoAdmin)
admin.site.register(DeletedImage, NameDeletedAdmin)
admin.site.register(FileRecord, FileAdmin)  ## must remove or unregister this model from photos
admin.site.register(NameIndex, NameIndexAdmin) ## 
admin.site.register(TidmarshRecord, TidmarshRecordAdmin)

admin.site.register(Profile)
admin.site.register(Upload)
admin.site.register(ChecklistNote, ChecklistAdmin)

admin.site.register(SpeciesPublished)
admin.site.register(ImagePublished, ImagesLog)
