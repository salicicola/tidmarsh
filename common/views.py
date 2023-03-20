import sys, django, os, datetime, xml.dom.minidom, time, email, urllib
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest,  HttpResponseNotFound, HttpResponseRedirect
from .bugs_views import *
VERSION = "0.1" ## adding RSS for bug report
VERSION = "0.1.0 (revno #45+) alpha" ##2021-02-19
VERSION = "0.1.1 (revno #52+) alpha" ##2021-02-20 adding RSS for bug report
VERSION = "0.1.2 (revno #55+) alpha" ##2021-02-20 bug reports improved, revno 8+
VERSION = "0.1.3  beta"

APPPATH = __file__
WORKING_DIR = os.getcwd()
print ("initializing", APPPATH, VERSION)
print ("working dir of common.views", WORKING_DIR)
BASE_DIR = "static/photos"
TEMP_DIRS = ["static/temp", "data/static/temp/scaled"]
if not os.path.exists(BASE_DIR):
    BASE_DIR = "data/static/photos"
    TEMP_DIRS = ["data/static/photos/temp", "data/static/photos/temp/scaled"]
if os.path.exists("/media/data/data/NewPhotos21"):
    PATTERN_DIR = "/media/data/data/NewPhotos"
else:
    PATTERN_DIR = None

print ("common.views [servlet] initialized, will use", BASE_DIR, TEMP_DIRS, "%s??" % PATTERN_DIR, "to search images")

if os.path.exists("data/static/images/notfound.png"):
    f = open("data/static/images/notfound.png", "rb")
    bad_png = f.read()
    f.close()
elif os.path.exists("static/images/notfound.png"):
    f = open("static/images/notfound.png", "rb")
    bad_png = f.read()
    f.close()
else:
    bad_png = None
if bad_png:
    print ("will send not found image")
else:
    print ("will send standard not found page for images")

def correct_imid(imid):
    print ("old style imid", imid,)
    a, bc = imid.split('$')
    b = bc[:5]
    c = "0%s" % bc[5:]
    imid = "%s%s%s" % (a, b, c)
    print ("corrected", imid)
    return imid        

def GetImage(request):
    imid = request.GET.get("id")
    if '$' in imid:
        imid = correct_imid(imid)
    y = imid[:4]
    m = imid[4:6]
    d = imid[6:8]
    path = "%s/%s%s/%s.jpg" % (BASE_DIR, y, m, imid)
    print ("testing", path, os.path.exists(path))
    if not os.path.exists(path):
        for temp_dir in TEMP_DIRS:
            path = os.path.join(temp_dir, imid + ".jpg")
            print ("testing", os.path.abspath(path), os.path.exists(path))
            if os.path.exists(path):
                break
    if not os.path.exists(path) and PATTERN_DIR:
        path = "%s%s/%s%s%s/%s.jpg" % (PATTERN_DIR, y[2:], y, m, d, imid)
        print ("testing", path, os.path.exists(path))
    if not os.path.exists(path):
        print ("will try external server")
        url = "http://172.104.19.75/servlet/GetImage?id=%s" % imid
        print (url)
        ret = urllib.request.urlopen(url)
        if ret.status == 200 and ret.getheader('Content-Type') == 'image/jpeg':
            img = ret.read()
            sdir = os.path.join("data/static/photos/%s" % imid[:6])
            if not os.path.exists(sdir):
                os.mkdir(sdir)
                print ("created", sdir)
            path = os.path.join("data/static/photos/%s/%s.jpg" % (imid[:6], imid))
            f = open(path, "wb")
            f.write(img)
            f.close()
            print (f)
            return HttpResponse(img, 'image/jpeg')
            ##return HttpResponseRedirect(url)
        else:
            if bad_png:
                print ("will send 404 with image", len(bad_png))
                return HttpResponseNotFound(bad_png, "image/png")
            else:
                print ("will send 404 html")
                return HttpResponseNotFound("not found") ## FIXME add not found GIF
    else:
        f = open(path, "rb")
        image = f.read()
        f.close()
        return HttpResponse(image, "image/jpeg")

## not yet in use
def sitemap(request):
    return render(request, "sitemap.htm")

### NEW defs needed for the web version + modified urls.py
def redirect_tidmarsh(request):
    path = request.path
    newpath = ""
    if 'map' in path:
        words = path.split('/')
        if path.endswith('/'):
            spid = words[-2]
        else:
            spid = words[-1]
        if spid.isdigit():
            newpath = "/photodb/tidmarsh/map/%s/" % spid
    if newpath:
        html = """<h2>All Tidmarsh related pages moved to <a href="/photodb/tidmarsh/">/photodb/tidmarsh/</a></h2>
                  <p>Try this <a href="%s">url</a> for the map</h2>""" % newpath
    else:
        html = """<h2>All Tidmarsh related pages moved to <a href="/photodb/tidmarsh/">/photodb/tidmarsh/</a></h2>"""
    return HttpResponseBadRequest(html)
""" valid urls
        /photodb/tidmarsh/map/15610/
    not valid from log:
        /tidmarsh/map/preview/plant/3152/
"""

def redirect_gallery(request, delay=7):
    path = request.path
    newpath = path.replace('mobile', 'view')
    newpath = "/photodb%s" % newpath
    url = newpath
    html = """<html><head><meta http-equiv="refresh" content="%s;URL='%s'" /></head><body><h2>Wrong address [%s].</h2> 
              <p>URL starting with /gallery/ are moved to /photodb/, but views for mobile devices are temporarily disabled.<br/>
                 If you are not redirected in a %s seconds, try this link 
                 <a href="%s">%s</a></p></body></html>
           """ % (delay, newpath, path, delay, newpath, newpath)
    return HttpResponseBadRequest(html)


