import sys, urllib.request
from django.test import TestCase
## new
from django.test import Client

## using Client(): Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.
## did not work, instead set SERVER_NAME
## https://midatlanticherbaria.org/ https://sernecportal.org/ https://nansh.org/
### Cullina, M.D., B. Connolly, B. Sorrie, and P. Somers. 2011. The vascular plants of Massachusetts: A county checklist, first revision. Massachusetts Natural Heritage & Endangered Species Program, Massachusetts Division of Fisheries and Wildlife, Westborough. 
### Sorrie, B.A. 1992. County checklist of Massachusetts plants. Unpublished.
### https://kiki.huh.harvard.edu/databases/specimen_search.php

TDM_URLS = """/photodb/tidmarsh/ /photodb/tidmarsh/checklist/ /photodb/tidmarsh/inaturalist/make/ 
    /photodb/tidmarsh/inaturalist/ /photodb/tidmarsh/introducing/ /photodb/tidmarsh/unwanted/
    /photodb/tidmarsh/map/bbox /photodb/tidmarsh/nonvascular/ /photodb/tidmarsh/vertebrates/
    /photodb/tidmarsh/invertebrates /photodb/tidmarsh/search/
""".split()
URLS2 = """http://localhost:8000/photodb/tidmarsh/gallery/view/17024/20151011olymp8158cs/ 
            http://localhost:8000/servlet/GetImage?id=20151011olymp8158cs
            http://localhost:8000/photodb/tidmarsh/gallery/view/12963/
            http://localhost:8000/photodb/tidmarsh/gallery/view/13017/
            http://localhost:8000/photodb/tidmarsh/gallery/view/15610/
            http://localhost:8000/photodb/tidmarsh/map/15610/
            http://localhost:8000/photodb/tidmarsh/map/?lat=41.916295&lon=-70.570503&plantname=Agalinis%20purpurea
            http://localhost:8000/photodb/tidmarsh/map/bbox/
            http://localhost:8000/photodb/tidmarsh/map/13433/
     http://localhost:8000/photodb/tidmarsh/gallery/view/17049/20140614samsu2419cs/    
     http://localhost:8000/photodb/tidmarsh/gallery/view/301492/20111004ricoh6214c/  
""".split()
##
BAD_URLS = """http://localhost:8000/servlet/GetImage?id=20150516samsu1342
            http://localhost:8000/photodb/tidmarsh/gallery/view/12358/20150516samsu1342/
     http://localhost:8000/servlet/GetImage?id=dsfdfs
     http://localhost:8000/servlXXXet/GetImage?id=dsfdfs 
""".split()

EXCLUDE_BAD = """http://localhost:8000/photodb/search/flag/exotic/

""".split()

## DID NOT WORK !!
def test1():
    passed = True
    errors = []
    c = Client(SERVER_NAME='localhost')
    for url in TDM_URLS:
        if url:
            url = "http://localhost:8000" + url
            response = c.get(url)
            print (response.status_code, url)
            if not response == 200:
                passed = False
                errors.append(url)
    print ("Passed?", passed)  
    print ("Errors?", errors)             

def test2(): ## outside Django
    passed = True
    errors = []
    for url in TDM_URLS:
        if url:
            url = "http://localhost:8000" + url
            code = urllib.request.urlopen("https://www.stackoverflow.com").getcode()
            print (code, url)
            if not code == 200:
                passed = False
                errors.append(url)
    for url in URLS2:
        if url:
            try:
                code = urllib.request.urlopen(url).getcode()
                print (code, url)
                if not code == 200:
                    passed = False
                    errors.append(url)
            except urllib.error.HTTPError:
                passed = False
                errors.append(url)
                print (sys.exc_info())
                print (url)
                ##raise
            except:
                errors.append(url)
                passed = False
                print (sys.exc_info())
                print (url)
                raise
    print ("Passed?", passed) 
    for err in errors: 
        print ("Errors?", err)             
