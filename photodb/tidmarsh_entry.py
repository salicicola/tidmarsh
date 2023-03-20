from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ## render_to_response, 
from django.template.loader import get_template
from django.template import Context
import sys, os, xml.dom.minidom, time, hashlib, datetime
from PIL import Image
from django.core.files.storage import FileSystemStorage
from . import EXIF_PIL
import time, xml.dom.minidom, sys, os, pickle, shutil
import lxml.etree as ET
try:
    from django.core.context_processors import csrf
except:
    from django.template.context_processors import csrf
import django
django_version = django.get_version()
from django.http import HttpResponseForbidden

from django.db import transaction

try:
    from .models import Profile
except:
    from tidmarsh.models import Profile
from django.contrib.auth.models import User


from .models import *
VERSION = "0.0.1 using XML"
VERSION = "0.0.3 using XML DB" ## via tomcat OK
VERSION = "0.1.8 using XML files for each user" ## , profile for image naming starting mobile, old retained
VERSION = "0.2.0 (testing)" ## XML files for each user, uid=filler
VERSION = "0.2.1 (fixing bugs)" ## 2018-05-12
VERSION = "0.2.2" ## 2018-05-18
VERSION = "0.2.5.0" ## with uploaded num from DB 2018-05-18, to 21 transaction, relational
VERSION = "0.3.0"   ## num from DB transaction, record unused
### (sample) salicis@willowlinode:~/sample$ python manage.py makemigrations >> Record Upload
### (sample) salicis@willowlinode:~/sample$ python manage.py migrate
## uwsgi.touch checked log ## errors: file_path
VERSION = "0.4.0" ## fixin bugs admin can edit
VERSION = "0.5.0" ## was broken: no uid in entry form, hence ....
VERSION = "0.6.0" ## moving to Django 2.* and Python 3.* (3.5) so far bugs: NaN in admin/1 because no \n between records
## cannot edit: missing /home/salicarium/django2/tidmarsh/XML/1.txt' errors with username for admin
VERSION = "0.6.2 (beta)" ## BETA adding diary/timesheet = worksheet
VERSION = "0.6.3 (beta)" ## BETA adding diary/timesheet = worksheet plus SQL
VERSION = "0.7.0 (beta)" ## 2019-07-12: all tables at the web, etc
VERSION = "0.7.3 (beta)" ## bug fixing, allow null hours + alpha assignements
VERSION = "0.7.4 (beta)" ## bug fixing, adding NurseryAssignment instead of text
VERSION = "0.7.5 (beta)" ## will improve and clean
VERSION = "0.7.6 (beta)" ## merging with linode
VERSION = "0.7.7 (beta)" ## merged and cleaned tdm partially (tdm_views)
VERSION = "0.8.0 (beta) [#28]" ## ready to sync with linode
VERSION = "0.9.1 (beta) [#29]" ## edited on linode: all TDM members can view DB/timesheet  
VERSION = "0.9.2 (beta) [#37]" ## see log file #37  
VERSION = "0.9.3 (beta) [#38]"
VERSION = "0.9.4 (beta) [#39]" ## fixed images in view (xslt)
VERSION = "0.9.5 (beta) [#40+]" ## redesigning url map
VERSION = "0.9.6 (beta) [#41+]" ## gallery to records, additional plantlist 2020-03-06
"""  add_gallery_records.py  add_gallery_records_log.html  added_tidmarsh.xml  added_tidmarsh_tuples.pickle  get_tdm_added.py.local
  out_record.2019.xml out_record.20200306.xml  templates/tidmarsh_adding.htm  templates/tidmarsh_monitor.htm """
VERSION = "0.9.7 (beta) [#50]" ## running checklist yet XML based but PhotoRecords table added
VERSION = "0.9.9 (beta)" ## to new webserver with new revno 8+, check views index
VERSION = "1.0.1 (beta)" ## added selected animals and salicicola plants gallery 2021-03-17

import logging
logger = logging.getLogger(__name__)


## new version standalone
gps_records = []
##FIXME set default/modify models:: verified = False
## tdm_entry_form_new.htm  ## not yey in use here
def tdm_entry_form_new(request, template="photodb/tidmarsh/tdm_entry_form_new.htm"):
    if not request.POST:
        return render (request, template, locals())
    elif request.GET:
        return HttpResponseBadRequest("no GET allowed")
    else:
        return save_tidmarsh_entry(request)

def save_tidmarsh_entry(request, template="photodb/tidmarsh/tdm_entry_form_new.htm"):
    global gps_records
    rid = TidmarshRecord.objects.latest("rid").rid + 1
    rec = TidmarshRecord()
    rec.rid = rid
    rec.actual_uid = request.user.username
    print (rec, rec.rid, rec.actual_uid)
    rec.coordinates = request.POST.get("coordinates", "")
    if request.POST.get("lcid"):
        rec.lcid = request.POST.get("lcid")
    else:
        rec.lcid = 'MA.TDM' ##FIXME
    rec.location = request.POST.get("location", "")
    rec.plantname = request.POST.get("plantname", "")
    rec.notes = request.POST.get("notes", "")
    rec.files  = request.POST.get("files", "")
    rec.photo_url  = request.POST.get("photo_url", "")
    rec.observed = request.POST.get("observed", "")
    rec.category = request.POST.get("category", "")
    rec.uid = request.POST.get("uid", "")
    rec.created = timezone.now() ## datetime.datetime.now()
    if request.POST.get("lat") and request.POST.get("lon"):
        try:
            lat = float(request.POST.get("lat"))
            lon = float(request.POST.get("lon"))
            rec.lat = lat
            rec.lon = lon
        except:
            print (sys.exc_info())
    try:
        rec.plant_id = int(request.POST.get("plant_id"))
    except:
        print (sys.exc_info())
    rec.user_agent = request.META.get('HTTP_USER_AGENT', "")
    if request.FILES:
        if rec.uid:
            uid = rec.uid
        else:
            uid = request.user.username
        ## pathicng relation
        rec.save() ## without pk cannot be saved perhaps
        url, phnum, newname, file_size, name, lat, lon, scaled = upload_image(request, uid, rec)
        if rec.files:
            value = rec.files
            rec.files = "%s %s" % (value, newname)
        else:
            rec.files = newname
        print ("uploaded", url, phnum, newname, file_size, name, lat, lon, scaled)
        print ("set files", rec.files)
        if lat and lon:
            rec.lat = lat
            rec.lon = lon
            print ("set latlon from the photo")
    if not rec.lat and not rec.lon:
        if rec.coordinates:
            lat, lon = rec.coordinates.split()
            try:
                lat = float(lat)
                lon = float(lon)
                rec.lat = lat
                rec.lon = lon
            except:
                pass
    rec.save()
    print ("saved", rec)
    fid = None
    if rec.lat and rec.lon and rec.plant_id:
        prec = (( rec.lat, rec.lon, rec.plant_id, "", 0, rec.lcid, fid))        
        if not gps_records or len(gps_records) < 1000:
            f = open("photodb/CACHE/gps_records.pickle", "rb")
            gps_records = pickle.load(f)
            print ("loaded", len(gps_records))
            f.close()
            gps_records.append(prec)
        shutil.copy2("photodb/CACHE/gps_records.pickle", "photodb/CACHE/gps_records.bak.pickle")
        f = open("photodb/CACHE/gps_records.pickle", "wb")
        pickle.dump(gps_records, f)
        print ("updated", f, len(gps_records), "gps recs")
        return HttpResponse("record saved and GPS caches updated [<a href='/photodb/tidmarsh/'>Home (Tidmarsh @ Salicicola Photodb)</a>]")
    else:
        return HttpResponse("record saved  [<a href='/photodb/tidmarsh/'>Home (Tidmarsh @ Salicicola Photodb)</a>]")
    ## for now only one record and cannot edit    
## end new blodk



##
def get_uid(request):
    if request.user.is_authenticated: ## python2 request.user.is_authenticated()
        print ("according to get_uid, authenticated", request.user, request.user.username)
        uid = request.user.username
    else:
        ##uid = None
        print ("according to get_uid, NOT authenticated", request.user, request.user.username)
        uid = "guest"
    ##print ("UID", uid)
    return uid   


## to be locked XXX FIXME BUT PROBABLY WORKED IN db
def save_ids(uid, rid, phnum):
####   out = open(os.path.join(os.path.dirname(__file__), "XML", uid + ".rid"), "w")
####   out.write(str(rid))
####   out.close()
####   ##print out
##   if phnum:
##       out = open(os.path.join(os.path.dirname(__file__), "XML", uid + ".phid"), "w")
##       out.write(str (phnum))
##       out.close()
##       ##print out
    pass
       

def normalize (s):
    return " ".join(s.strip().split())


def scale_image(img, phid, size=(500,500)):
    try:
        img.thumbnail(size, Image.ANTIALIAS)
        outname = "%sa.jpg" % phid
        outpath = "data/static/uploaded/%s" % outname
        img.save(outpath, "JPEG")
        return outname
    except:
        print (sys.exc_info())
        logger.exception("cannot scale image")
        ## raise
        return None

## FIXME
## see https://medium.com/@hakibenita/how-to-manage-concurrency-in-django-models-b240fed4ee2
##from django.utils.decorators import classmethod
##@classmethod
## to models? and ...
##@transaction.atomic cannot save twice with transaction

@transaction.atomic
def start_upload(request, uid):
    f= request.FILES["file"]
    fs = FileSystemStorage()
    ##  saved OK but return wrong URL not absolute but with starting /
    ## debugging should set params in setting for MEDIA_ROOT and MEDIA_URL
    print ("fs.location", fs.location)
    ## correct in both djangos, here from django.core.files.storage import FileSystemStorage
    file_path = "data/static/uploaded/%s.jpg" %  str(time.time()).replace('.', '')
    filename = fs.save(file_path, f) ## , max_length=1024*1024*1024*5
    up = Upload()
    up.origname = f.name ##
    up.tempname = os.path.split(filename)[1]
    up.savedname = ""
    up.size = os.path.getsize(file_path)
    up.browser = request.META.get("HTTP_USER_AGENT", "")
    if len(uid) > 5:
        up.uid = uid[:5] ## correcting 2021-12-15
    else:
        up.uid = uid
    ##up.actual_uid = get_uid(request) ## 0.4.0
    up.submitted_by = get_uid(request) ## correcting 2021-12-15
    try:
        ##print ("temp image", file_path, os.path.exists(file_path))
        ##print ("will try to change permissions")
        ##os.chmod(file_path, "0o644") ## python 2: 0644
        os.system("chmod 644 %s" % file_path)
        print ("done? chmod")
    except:
        print (sys.exc_info())
        print ("cannot  chmod")
        logger.error("cannot chmod", exc_info=True)
    url = fs.url(filename)
    print ("debug FileStorage, got url", url)
    print ("PATCHING")
    if url.startswith("/data/static"):
        url = "%s%s"% (fs.location, url)
    print ("patched", url)
    orname = f.name
    f.close()
    up.save()
    ## No such file or directory: '/data/static/uploaded/16395985047801418.jpg in checking its size
    print (up, url, file_path)
    return (up, url, file_path)
####
def get_exif(img):
    ##print ("running get_exif for", img)
    try:
        exif_data = EXIF_PIL.get_exif_data(img)
        lat, lon = EXIF_PIL.get_lat_lon(exif_data)
        ##up.latlon = "%s,%s" % (lat, lon)
    except:
        lat, lon = None, None
        exif_data = None
    ##print ("returning", exif_data, lat, lon)
    return (exif_data, lat, lon)


""" 
  perhaps somewhere here warning [at least in Python 3.4 in 3.6 will be an error?]: 
  ''' /home/salicarium/Env/py34/lib/python3.4/site-packages/dateutil/parser/_parser.py:1206: UnknownTimezoneWarning: tzname PDT identified but not understood.  Pass `tzinfos` argument in order to correctly return a timezone-aware datetime.  In a future version, this will raise an exception.
  category=UnknownTimezoneWarning) '''
 :::: example ::::
 	from dateutil.tz import gettz
	from dateutil.parser import parse
	parse('Wed May 20 13:51:10 PDT 2015',  tzinfos={'PDT': gettz('America/Los_Angeles'),
                           'PST': gettz('America/Los_Angeles')})
"""    
def upload_image(request, uid, ref_obj=None, use_uid=False):
    if uid == 'gid':
        alias = "gidav"
    else:
        alias = uid
    up, url, file_path = start_upload(request, uid)
    ##pathcing missing rel
    up.record = ref_obj
    up.save()
    phnum = up.id
    file_size = os.path.getsize(url) ## No such file or directory: '/data/static/uploaded/16395985047801418.jpg'
    img = Image.open(url)
    exif_data, lat, lon = get_exif(img)
    if lat and lon:
        up.latlon = "%s %s" % (lat, lon)
    if exif_data  and 'DateTimeOriginal' in exif_data: ## has_key('DateTimeOriginal')
        try:
            up.taken = exif_data["DateTimeOriginal"]
            ##print (up.taken)
            up.save()
            ##print ("saved 1")
        except:
            try:
                dt, tm = exif_data["DateTimeOriginal"].split()
                dt = dt.replace(':', '-')
                up.taken = "%sT%s" % (dt, tm)
                ##print ("2", up.taken)
                up.save()
                ####print "saved 2"
            except:
                ##print "catch error"
                ##print sys.exc_info()
                pass
        if 'Make' in exif_data: ## .has_key()
            alias = exif_data['Make'][:5].lower()
        ### FIXME if num > 9999
        if use_uid and len(uid) > 4:
            ##print "re-inforce using uid instead of exif data", alias
            alias = uid[:5]
        newname = "%s%s%s.jpg" % (str(exif_data["DateTimeOriginal"].replace(':', '')[:8]), alias, "%04d" % phnum)
    else:
        date = datetime.date.today().isoformat().replace('-', '')
        newname = "%s%s%s.jpg" % (date, alias, "%04d" % phnum)
    new_path = "data/static/uploaded/%s" %  newname
    try:
        os.rename(file_path, new_path)
        ##print "FIXME: renamed"
    except:
        ##print sys.exc_info()
        pass
    scaled = scale_image(img, os.path.splitext(newname)[0])
    ##print "scaled to", scaled
    up.savedname = os.path.split(new_path)[1]
    up.savedname = newname
    if scaled:
        up.scaled = "a"
    up.uploaded = datetime.datetime.now()
    origname = up.origname
    up.save()
    ##print up    
    if scaled:
        return (url, phnum, newname, file_size, origname, lat, lon, scaled)
    else:
        return (url, phnum, newname, file_size, origname, lat, lon, "") ## had an typos fixed

def append_value(elem, att, value):
    old_value = elem.getAttribute(att)
    new_value = "%s %s" % (old_value, value)
    elem.setAttribute(att, new_value.strip())

def get_rids(uid):
    rids = []
    fname = "tidmarsh/XML/%s.txt" % uid
    if os.path.exists(fname):
        f = open(fname)
        x = "<r>%s</r>" % f.read()
        f.close()
        dom = xml.dom.minidom.parseString(x)
        for r in dom.getElementsByTagName("record"):
            rid = int(r.getAttribute("rid"))
            if not rid in rids:
                rids.append(rid)
                ##print "added", rid
    rids.sort()
    return rids
    
def save_entry(request):
    rid = request.POST.get("rid") 
    uid = request.POST.get("uid") ## 0.4.0 but if ...
    actual_uid = get_uid(request) ## 0.4.0
    rec = xml.dom.minidom.parseString("<record/>")
    rec.documentElement.setAttribute("user_agent", request.META.get("HTTP_USER_AGENT", ""))
    if rid:
        print ("edit mode, rid ", rid)
    else:
        rids = get_rids(uid)
        if rids:
            rid = max(rids) + 1
        else:
            rid = 1
        ##print "new record, rid", rid, "set attribute here"
        rec.documentElement.setAttribute("observed", datetime.date.today().isoformat())      
    rec.documentElement.setAttribute("rid", str(rid))
    ##print "currently", rec.toxml()
    if request.FILES:
        url, phnum, newname, file_size, name, lat, lon, scaled = upload_image(request, uid)
        ##print "with file upload"
    else:
        url, phnum, newname, file_size, name, lat, lon, scaled = "", 0, "", 0, "", None, None, ""
        ##print "without file upload"
    for k, value in request.POST.items():
        ##print k, value
        if not "csrf" in k:
             rec.documentElement.setAttribute(k, normalize(value))    
    rec.documentElement.setAttribute("rid", str(rid)) ## rid may be empty in request
    ##print "now", rec.toxml()
    if url:
        if scaled:
            append_value(rec.documentElement, "files", scaled)
        else:
            append_value(rec.documentElement, "files", newname)
        append_value(rec.documentElement, "filesize", file_size)
        append_value(rec.documentElement, "origname", name)
        if not request.POST.get("lat"):
            if lat and lon:
                rec.documentElement.setAttribute("lat", str(lat))
                rec.documentElement.setAttribute("lon", str(lon))
        else:
            pass
            ##print ("skip setting lat/lon")
    ##print "almost finally", rec.toxml()
    ##out = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"), "a")
    ##out = open(os.path.join("photodb/tidmarsh", "XML", request.POST.get("uid", uid) + ".txt"), "a")
    out = open(os.path.join("photodb/tidmarsh", "XML", "xxx.txt"), "a")
    ##out = open(os.path.join("data", "XML", request.POST.get("uid", uid) + ".txt"), "a")
    if not rec.documentElement.getAttribute("rid"):
        ##print "FATAL ERROR, @rid not set"
        ##print rec.toxml()
        raise IOError ("no rid")
    rec.documentElement.setAttribute("created", datetime.datetime.now().isoformat())
    ##print "finally", rec.toxml()
    out.write(rec.documentElement.toxml())
    out.write("\n")
    out.close()
##    save_ids(uid, rid, phnum)
    url = "/tidmarsh/entry/%s/%s/" % (uid, rid)
    ##print "finished saving", rec.documentElement.toxml()
    return HttpResponseRedirect(url)

def _find_record(request, uid, rid):
    ##f = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"))
    f = open(os.path.join("data", "XML", request.POST.get("uid", uid) + ".txt"))
    ##print f
    sxml = ""
    rids = []
    for line in f.readlines():
        if line.strip():
            words = line.strip().split()
            ##print words
            for word in words:
                if "rid=" in word:
                    try:
                        _rid = word.split('rid="')[1]
                        ##print _rid,
                        _rid = _rid.split('"')[0]
                        ##print _rid
                        if not _rid in rids:
                            rids.append(int(_rid))
                        if _rid == rid:
                            sxml = line.strip()
                            ##print _rid, rid, sxml
                    except:
                        print (sys.exc_info())
                    break
    f.close()
    ##print "last record for", uid, rid
    ##print sxml
    return sxml

def question(request, uid="", rid="", mobile=True):
    print (__file__, "question()", uid, rid, "mobile", mobile)
    ##print request.GET
    ##print request.META["HTTP_USER_AGENT"]
    c = {"django_version": django_version}
    if request.GET.get('m'):
        c["mobile"] = request.GET.get('m')
    else:
        c["mobile"] = mobile
    if c["mobile"]:
        template = "tdm_entry_form.htm"
    else:
        template = "tdm_qaa_add.htm"
    actual_uid = get_uid(request)
    user = User.objects.get(username = actual_uid)
    try:
        prof = Profile.objects.get(user = user)
    except:
        prof = None
        print ("XXX Profile matching query does not exist")
    c["actual_uid"] = actual_uid
    ##print prof, prof.phidcode

    c["phidcode"] = prof.phidcode
    ##print "FIXING EMPTY uid", uid, actual_uid
    if not uid:
        uid = actual_uid
    ##print "FIXED EMPTY uid", uid, actual_uid
    c["uid"] = uid  ## None if not authenticated XXX: to add get_authorized(uid) ## THIS IS WRONG SHOULD BE GUEST
    c["rid"] = rid
    c["version"] = VERSION
    try:
        c.update(csrf(request))
    except:
        pass
    if not rid:
        ##print "entry new record"
        if request.GET:
            ##print request.GET
            c["location"] = request.GET.get("location", "")
            c["lcid"] = request.GET.get("lcid", "")
            c["coordinates"] = request.GET.get("coordinates", "")
            c["plantname"] = request.GET.get("plantname", "")
            c["plant_id"] = request.GET.get("spid", "")
            c["category"] = request.GET.get("category", "")
            ##print c
        return render(request,template, c)
    else:
        sxml = _find_record(request, uid, rid)
        if not sxml:
            raise IOError("cannot find XML record")
        else:
            dom = xml.dom.minidom.parseString(sxml)
            doc = dom.documentElement
            for att in doc.attributes.items():
                ##print att
                c[att[0]] = att[1]
            ##print c
            return render(request, template, c)


##xsl_filename = os.path.join(os.path.dirname(__file__), "XML", "view.xslt")
##xslt = ET.parse(xsl_filename)
##transform = ET.XSLT(xslt)


## committing with too many flaws yet

def view_record(request, uid, rid):
    ##print "running", __file__, uid, rid
    f = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"))
    sxml = ""
    rids = []
    actual_uid = get_uid(request)
    if uid == actual_uid == "guest":
        mode = "test_admin"
    elif actual_uid == "admin":
        mode = "admin"
    elif actual_uid == uid:
        mode = "owner"
    else:
        mode = "forbidden"
    ##print uid, "accessed by", actual_uid, "mode", mode
    for line in f.readlines():
        if line.strip():
            words = line.strip().split()
            for word in words:
                if "rid=" in word:
                    try:
                        _rid = word.split('rid="')[1]
                        ##print _rid,
                        _rid = _rid.split('"')[0]
                        ##print _rid
                        if not _rid in rids:
                            rids.append(int(_rid))
                        if _rid == rid:
                            sxml = line.strip()
                            ##print _rid, rid, sxml
                    except:
                        print (sys.exc_info())
                    break
    f.close()
    ##print "last record for", uid, rid
    ##print sxml
    minrid = min(rids)
    maxrid = max(rids)
    try:
        dom = ET.fromstring(sxml)
    except:
        dom = ET.fromstring("""<record category="m" coordinates="" created="" file="" lat="" lcid="" location="" lon=""
                    notes="RECORD NOT SAVED CORRECTLY to navigate to another record change URL manually. Ask admin to fix it." observed="" photo_url=""
                            plant_id="" plantname="" rid="" uid="" user_agent=""/>""")
    dom.set("max", str(maxrid))
    dom.set("min", str(minrid))
    ##print dom
    xsl_filename = os.path.join(os.path.dirname(__file__), "XML", "view.xslt")
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    ##newdom = transform(dom, **{"mode":mode}) ## did now work mode=mode
    ##newdom = transform(dom, mode=ET.XSLT.strparam("str_example")) ## this way works
    newdom = transform(dom, mode=ET.XSLT.strparam(mode))
    ##print "by", mode
    print ("DEBUG", dom, "lat=", dom.get("lat"), "lon=", dom.get("lon"), "explicit", dom.get("coordinates"))
    html = ET.tostring(newdom, pretty_print=True)
    return HttpResponse(html)

##from .models import TestRecord
def get_records_xml(request, uid, action="commit"):
    print ("Start running ADMIN functions:", __file__, uid, action)
    if request:
        actual_uid = get_uid(request)
    else:
        actual_uid = "admin"
        print ("enforce admin since using command line")
    print ("actual uid")
    if uid == actual_uid == "guest":
        mode = "test_admin"
    elif actual_uid == "admin":
        mode = "admin"
    elif actual_uid == uid:
        mode = "owner"
    else:
        mode = "forbidden"
    print (uid, "accessed by", actual_uid, "mode", mode)
    if 'admin' in mode or mode=='owner':
        lock = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".lock"), "w")
        lock.close
        print ("lock created", lock)
        f = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"))
        lines = f.readlines()
        f.close()
        ## XXX
        out = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".bak"), "a")
        for line in lines:
            out.write("%s\n" % line)
        out.close()
        print ("backup created", out)
        data_path = os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt")
        f = open(data_path, "w")        
        f.close()
        print ("original file cleaned", f, os.path.getsize(data_path))
        print ("starts normalizing test", len(lines))
        clean_lines = {}
        clean_xml = xml.dom.minidom.parseString("<records cleaned='%s'/>" % datetime.datetime.now().isoformat())
        print (clean_xml.toxml())  ## passed     
        for line in lines:
            dom = None
            if line.strip():
                try:
                    dom = xml.dom.minidom.parseString(line.strip())
                    doc = dom.documentElement
                    rid = int(doc.getAttribute("rid"))
                    clean_lines[rid] = doc.toxml()
                    print (rid, "added")
                except:
                    ##print "??????", line.strip()
                    print (sys.exc_info())
                    print (line.strip())  ## FIXME were two records per line !
                    raise
        new_text = []
        keys = clean_lines.keys()
        ## XXX: dict_keys' object has no attribute 'sort' ## python 3
        keys = list(keys) ## fixing ???
        keys.sort()
        print ("keys", keys)
        for k in keys:
            _text = clean_lines[k]
            if ' delete=' in _text and action=="commit": ## FIXME NOT ENOUGH ROBUST
                print ("DELETED", _text)
            else:
                new_text.append(_text)
                print ("appended")
##        for items in clean_lines.items():
##            new_text.append(items[1])
        print ("HERE so far")
        new_text = "\n".join(new_text)
        new_xml_text = "<records cleaned='%s'>%s</records>" % (datetime.datetime.now().isoformat(), new_text)
        new_xml = xml.dom.minidom.parseString(new_xml_text)
        out_text = "<html><head></head><body><h2 style='margin-bottom:0'>Records created and unless entered by guest account, they should have been saved</h2>"
        out_text += "<h3 style='margin-top:0'>(If saved, first number in each line refer to saved record ID, last number to ID of uncommitted records)</h3>"
        if action == "commit" and 'admin' in mode:
            for rec in new_xml.getElementsByTagName("record"):
                r = TestRecord()
                ##r.rid = rec.getAttribute("rid")
                r.plant_id = rec.getAttribute("plant_id")
                r.plantname = rec.getAttribute("plantname")
                r.lcid = rec.getAttribute("lcid")
                r.location = rec.getAttribute("location")
                r.lat = rec.getAttribute("lat")
                r.lon = rec.getAttribute("lon")
                r.coordinates = rec.getAttribute("coordiantes")
                r.save()
                ##print r
                out_text += "<div>%s [from rec #%s]</div>" % (r, rec.getAttribute("rid"))
        else:
            out = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"), "w")
            for line in new_text:
                out.write("%s" % line) ## fixing bug, needs HardReturn at the end
            out.write("\n") ## FIXME : fixing
            out.close()
            print ("clean data file recreated", out)
        out_text += "</body></html>"
        os.unlink(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".lock"))
        print ("lock released")         
        ##return HttpResponse(new_xml.toxml(), "text/xml")
        if action == 'commit':
            return HttpResponse(out_text)
        else:
            return HttpResponse(new_xml.toxml(), "text/xml")
    else:
        return HttpResponse("not authorized for this action")
    
def set_attribute(request, uid, rid, action="verified"):
    ##print "running set attribute for", __file__, uid, rid, action
    caller = request.META['HTTP_REFERER']
    ##print caller
    f = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"))
    sxml = ""
    rids = []
    actual_uid = get_uid(request)
    if uid == actual_uid == "guest":
        mode = "test_admin"
    elif actual_uid == "admin":
        mode = "admin"
    elif actual_uid == uid:
        mode = "owner"
    else:
        mode = "forbidden"
    ##print uid, "accessed by", actual_uid, "mode", mode
    ##if not 'admin' in mode or not mode=='owner':
    ##    return HttpResponse("not authorized for this action")
    if 'admin' in mode or mode == 'owner':
        ##print "authorized"
        for line in f.readlines():
            if line.strip():
                words = line.strip().split()
                for word in words:
                    if "rid=" in word:
                        try:
                            _rid = word.split('rid="')[1]
                            ##print _rid,
                            _rid = _rid.split('"')[0]
                            ##print _rid
                            if not _rid in rids:
                                rids.append(int(_rid))
                            if _rid == rid:
                                sxml = line.strip()
                                ##print _rid, rid, sxml
                        except:
                            print (sys.exc_info())
                        break
    else:
        return HttpResponse("not authorized")
    f.close()
    ##print "last record for", uid, rid
    ##print sxml
    doc = xml.dom.minidom.parseString(sxml).documentElement
    if action == "unverify":
        doc.removeAttribute("verified")
    elif action == "restore":
        doc.removeAttribute("delete")
    else:
        doc.setAttribute(action, actual_uid)
    out = open(os.path.join(os.path.dirname(__file__), "XML", request.POST.get("uid", uid) + ".txt"), "a")
    out.write("\n") ## hopefully will fix ~ "junk after document element: line 1, column 436"
    out.write(doc.toxml())
    out.write("\n") ## maybe not needed but ...
    out.close()
    if caller:
        return HttpResponseRedirect(caller)
    else:
        return HttpResponse(doc.toxml(), "text/xml")

##from tidmarsh.views
DJANGO_VERSION = "" ## FIXME
def entry_awc(request, mobile=True):
    django_version = DJANGO_VERSION
    version = VERSION
    dom = xml.dom.minidom.parse(open("data/static/KML/planted/awc_pods.xml"))
    pods = []
    for loc in dom.getElementsByTagName("location"):
        lon, lat = loc.getAttribute("pnt").split(',')
        lon = lon[:9]
        lat = lat[:8]
        pods.append({"lcid": loc.getAttribute("lid"),
                     "coordinates": "%s %s" % (lat, lon),
                     "lat": lat, "lon": lon })
    ##print (pods)
    return render(request, "awc_pods.htm", locals())

