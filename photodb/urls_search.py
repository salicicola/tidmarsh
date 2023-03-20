from django.urls import path
from . import search2 as search

##/photodb/search/
urlpatterns = [
        path('colname/<str:colname>/', search.search_colname), ## draft
        path('latname/<str:latname>/', search.search_latname),  ## stub
        path('flag/<str:flag>/', search.search_flag), ## stub
        ## by flags out of scope exotic, cultivated, domestic
        path('', search.search_photos),
        path('imid/<str:imid>/', search.get_all_photos),
        path('photos/by/', search.get_by_others),
        path('tags/', search.get_tags),
]


