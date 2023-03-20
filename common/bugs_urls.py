from django.urls import path
from .bugs_views import *

urlpatterns = [
    path('', bugs_index), ## same as old /bugs/ not retained in main urls.py # template="bugs/bugentry.htm"
    path('entry/', bug_entry), ## same as old /bug/ retained in main urls.py
    path('view/', view_all_bugs), ## depends on authentication and/or claimed user ID # "bugs/submitted.htm"
    path('view/<str:submitted>/', view_all_bugs),
    path('edit/', edit_bug), ## >> manage_bug() >> delete() or commit() and delete() # "bugs/edit_bug.htm"
    path('manage/', manage_bug), ## same as old /bug/manage/
    path('rss/bug/', view_bug_rss), ## same as old /rss//bug/
    path('401/', disallowed),
]

## in main urls.py, so far::
##    path('bugs/', include('common.bugs_urls')),
##    path('bug/', bugs_views.bug_entry),
##    path('bug/manage/', bugs_views.manage_bug),
##    path('rss/bug/', bugs_views.view_bug_rss),

##in models.BugRecord fields:: product component version user_name submitted_by severity hardware OS summary description url
