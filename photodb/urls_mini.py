import sys
from django.urls import path, include ##, re_path
from . import views, views_nonvascular, views_nonlegacy, edit

## SPECIFIC for Tidmarsh: commented not needed
urlpatterns = [   
    path('tidmarsh/', include ('photodb.urls_tidmarsh')),
    path('search/', include ('photodb.urls_search')),
    path('gallery/note/<int:pnid>/', views.show_note),
    path('gallery/mobile/<int:spid>/', views_nonvascular.species_mobile),
    path('gallery/mobile/<int:spid>/<str:imid>/', views_nonvascular.imgview_mobile),
    path('gallery/view/<int:pnid>/', views_nonlegacy.view_photo_records, {'legacy':False, "template":"photodb/photos/gallery_index.htm", "public":True}),
    path('gallery/view/<int:fid>/<int:pnid>/', views_nonlegacy.view_photo_records, {'legacy':False, "template":"photodb/photos/gallery_index.htm", "public":True}),
    path('gallery/view/<int:spid>/<str:imid>/', views.image_view, {"legacy":False}),
	path('edit/name/<int:pnid>/', edit.edit_name_mini),
	path('identify', edit.identify),
	path('getoptions/<int:fid>/', edit.identify_get_names), 
	path('saveID/', edit.identify_save),
	path('add_genus_species/', edit.add_genus_species),
	path('copyto/', edit.copy_to),
	path('copyto/save/', edit.save_copied),
	path('edit/caption/', edit.CaptionEditor),  
    path('edit/delete/<int:pnid>/', edit.delete_name_legacy_name),
    path('add/synonym/<int:spid>/', edit.add_syn),
]
try:
    from . import entry, entry_test, admin_thums ## needs .Thumbnails, hardcoded image source: tomcat.ROOT
    urlpatterns.extend( [
        path('missing/thumbs/', admin_thums.make_missing_thumbnails),
        ## for local usage, could be PC specific 
    	path('entry/from/<str:fname>', entry.save_from),
	    path('entry/legacy/', entry_test.entry_form, {"template": "photodb/entry_legacy.htm"}),
	    path('entry/new/', entry_test.entry_form, {"template": "photodb/entry_new.htm"}),

	    path('entry/legacy/<str:fname>',  entry_test.send_image),
	    path('entry/legacy/delete/<str:fid>/', entry_test.move_deleted_photo),
	    path('entry/savephoto', entry_test.save_photo_records),
	    path('delete/<str:imid>/', entry_test.move_deleted_photo),
	    path('entry/single/', entry_test.entry_one), ## supply tomcat path to image as path=
    ] )
    print ("added entry module")
except:
    print (sys.exc_info())
    print ("cannot use entry modules")

