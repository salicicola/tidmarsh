from django.shortcuts import render
import xml.dom.minidom, os, datetime, sys, time
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import *
try:
    from names.models import CommonName, Name, SpeciesMeta
except:
    print ("should be available here")
try:
    from common.models import Town, Location
except:
    print (Town, Location, "from .models")
MONTHES = "January February March April May June July August September October November December".split()


VERSION = "0.1: prototype (by common name)"
VERSION = "0.2: prototype" ## add photos with limitations
VERSION = "0.2.1 (2021-10-28)" ## add form for photo search 
VERSION = "0.2.2 (2021-10-30)" ## add search by plant name == spid
VERSION = "0.2.3 (2021-11-01)"
VERSION = "0.2.4 (2021-11-02)" ## prototype to alpha #196+
VERSION = "0.2.5 (2021-11-02)" ## alpha #198+
VERSION = "0.2.6 (2021-12-08)" ## restored and somewhat improved
VERSION = "0.2.8 (2022-03-06)"
VERSION = "0.2.9 (2022-03-06)" ## returning to using introduced OR invasive field for flag searching: nonnative can be deleted
VERSION = "0.3.0 (2022-03-06)" ## nonnative field removed use only introduced + two invasive ##115+

def get_all_photos(request, imid=""):
    version = VERSION
    print ("running searc.get_all_photos() for", imid)
    if not imid:
        imid = request.GET.get("imid")
    if not imid:
        return HttpResponseBadRequest("no imid supplied")
    q1 = VascularImage.objects.filter(imid__contains=imid)
    print ("found", len(q1), "by", imid)
    q2 = NonVascularImage.objects.filter(imid__contains=imid)
    print ("found", len(q2), "by", imid)
    q3 = AnimalImage.objects.filter(imid__contains=imid)
    print ("found", len(q3), "by", imid)
    q4 = VariaImage.objects.filter(imid__contains=imid)
    print ("found", len(q4), "by", imid)
    ##q = q1 | q2 | q3 | q4
    ##print ("total found", len(q1), "by", imid)
    ## Cannot combine queries on two different base models
    ## or q = q1.union(q2,q3) # more than 2 queryset union without duplicates   
    q = list(q1)
    q.extend(list(q2))
    q.extend(list(q3)) ##.extend(list(q3)).extend(list(q4))
    q.extend(list(q4))
    rset = q
    print ("total found YET UNSORTED", len(q), "by", imid)
    return render(request, "photodb/results_photos.htm", locals())


## XXX rabochi draft to add attribute authorships
def get_by_others(request):
    q1 = VascularImage.objects.filter(caption__icontains='photo credit')
    q2 = NonVascularImage.objects.filter(caption__icontains='photo credit')
    q3 = AnimalImage.objects.filter(caption__icontains='photo credit')
    q4 = VariaImage.objects.filter(caption__icontains='photo credit')
    q = list(q1)
    q.extend(list(q2))
    q.extend(list(q3)) ##.extend(list(q3)).extend(list(q4))
    q.extend(list(q4))
    print ("total found YET UNSORTED", len(q), "not salicicola")
    authors = []
    for rec in q:
        author = ""
        try:
            author = rec.caption.split('Photo credit')[1]
            ##print (author, rec)
        except:
            try:
                author = rec.caption.split('photo credit')[1]
            except:
                print (rec.caption)
                raise
        if ',' in author:
            author = author.split(',')[0]
        if ';' in author:
            author = author.split(';')[0]
        if '***' in author:
            author = author.split('***')[0]
        if ']' in author:
            author = author.split(']')[0]
        if "Toni Roberson" in author:
            author = "Toni Roberson"
            print ("corrected", author)
        author = author.strip()     
        if not author in authors:
            authors.append(author)
        rec.author = author
    data = []
    authors.sort()
    for author in authors:
        r = (author, [])
        ##print (r)
        for rec in q:
            ##print (rec.author, '>=?', author)
            if rec.author == author:
                r[1].append(rec)
                ##print ("appended")
        data.append(r)
    ##print (data)
    return render(request, "photodb/results_contributors.htm", locals())

def get_manager(category):
    if category == 'vascular':
        return VascularImage.objects
    elif category == 'nonvascular':
        return NonVascularImage.objects
    elif category == 'animals':
        return AnimalImage.objects
    elif category == 'varia':
        return VariaImage.objects
    else:
        return None ### XXX should raise something


## so far for only one spid, lcid, town
def get_photos(imid="", spid="", lcid="", town="", year=0, month="", day=0, category="", authenticated=True):
    rset = None
    manager = get_manager(category)
    if not manager:
        return HttpResponseBadRequest("wrong category: %s" % category)
    print ("will use manager", manager, type(manager))
    if imid:
        if not rset:
            rset = manager.filter(imid__contains=imid)
        else:
            rset = rset.filter(imid__contains=imid)
        print ("got %s photos by imid part" % len(rset))
        if not rset: return rset
    if spid:
        if not rset:
            rset = manager.filter(plant__pnid=int(spid))
        else: 
            rset = rset.filter(plant__pnid=int(spid))
        print ("got %s photos by spid" % len(rset))
        if not rset: return rset
    if year:
        if not rset:
            rset = manager.filter(imid__startswith=str(year))
        else:
            rset = rset.filter(imid__startswith=str(year))
        print ("got %s photos by year" % len(rset))
        if not rset: return rset
    if month:
        ## FIXME month should be a string
        try:
            if month.isdigit():
                month = int(month)
                month = MONTHES[month-1]
                print ("got month from number", month)
            else:
                month = month.strip().capitalize()
                print ("got month from string", month)
                if month not in MONTHES:
                    print ("wrong name of month")
                    return HttpResponseBadRequest("wrong month '%s'" % month)
        except:
            print ("%s" % str(sys.exc_info()))
            return HttpResponseBadRequest(month)        
        if not rset:
            rset = manager.filter(date__startswith=month)
        else:
            rset = rset.filter(date__startswith=month)
        print ("filtered by month, got", len(rset))
        if not rset: return rset
    if day:
        day = " %s," % day
        if not rset:
            rset = manager.filter(date__endswith=day)
        else:
            rset = rset.filter(date__endswith=day)
        print ("filtered by day, got", len(rset))
        if not rset: return rset
    if lcid:
        if not rset:
            rset = manager.filter(lcid_temp__contains=lcid)
        else:
            rset = rset.filter(lcid_temp__contains=lcid)
        print ("filtered by lcid, got", len(rset))
        if not rset: return rset
    if town:
        lcid = Town.objects.get(town=town).locID
        print ("found location ID for town", lcid)
        tokens = lcid.split(".")
        town_lcid = ".%s." % tokens[-1]
        if not rset:
            rset = manager.filter(lcid_temp__contains=town_lcid)
        else:
            rset = rset.filter(lcid_temp__contains=town_lcid)
        print ("filtered by town, got", len(rset))
        if not rset: return rset
    print ("nearly ready to pass record set", len(rset))
    if not authenticated:
        rset = rset.exclude(nr__lte=0).exclude(nr__gte=100)
        print ("not authenticated will use only published photos", len(rset))
    return rset

## restoring 
def search_photos(request, category=None, output="html"):
    authenticated = request.user.is_authenticated
    print ("search_photos authenticated user?", authenticated)
    version = VERSION 
    if request.POST or request.FILES: ## or ... except HEAD
        return HttpResponseBadRequest("only GET/HEADER is allowed")
    if not request.GET:
        return render (request, "photodb/search_photos.htm", locals())
    imid = request.GET.get("imid", "").strip()
    spid = request.GET.get("spid", "").strip()
    lcid = request.GET.get("lcid", "").strip()
    town = request.GET.get("town", "").strip()
    year = request.GET.get("year", "").strip()
    month = request.GET.get("month", "").strip()
    day = request.GET.get("day", "").strip()
    if not imid and not spid and not lcid and not town and not year and not month and not day:
        return HttpResponseBadRequest("no search params provided")
    if not category:
        category = request.GET.get("category", "").strip()
        if not category:
            return HttpResponseBadRequest("one of categories (vascular nonvascular animals varia) must be provided")
        if not category in "vascular nonvascular animals varia".split():
            return HttpResponseBadRequest("wrong category [%s] provided" % category)
    rset = get_photos(imid, spid, lcid, town, year, month, day, category, authenticated)
    print ("recieved rset as type of", type(rset))
    print (isinstance(rset, HttpResponse))
    if isinstance (rset, HttpResponse):
        return rset
    if not rset:
        return HttpResponseBadRequest("nothing found")   
    if output == "html":
        ## new
        names = {}
        print ("will process rset", type(rset))
        rset = rset.order_by("plant__upper__latnname").order_by("plant__latname")
        print ("rset sorted")
        for rec in rset:
            latname = "%s %s" % (rec.plant.upper.latname, rec.plant.latname)
            colnames = rec.plant.colnames
            name = "%s (%s)" % (latname, colnames)
            if name in names:
                names[name].append((rec.spid, rec.imid, rec.genname, rec.latname, rec.location))
            else:
                names[name]= [(rec.spid, rec.imid, rec.genname, rec.latname, rec.location),]
##            if rec.genname in rec.latname:
##                latname = rec.latname
##            else:
##                latname = "%s %s" % (rec.genname, rec.latname)
##            if latname in names:
##                names[latname].append((rec.spid, rec.imid, rec.genname, rec.latname, rec.location))
##            else:
##                names[latname] = [(rec.spid, rec.imid, rec.genname, rec.latname, rec.location)]
        names = names.items()
        names = list(names)
        names.sort()
        return render (request, "photodb/results_photos2.htm", locals())
        ##return render (request, "photodb/results_photos.htm", locals())
        ##return HttpResponse(html)
    else:
        HttpResponseBadRequest("bad or not implemented output method requested (use 'html')")
""" bugs: 
when using http://192.168.1.9:9090/photodb/search/photos/?lcid=MA.GRR&spid=6001&town=Williamstown
one of links: DoesNotExist at /gallery/view/000/6001/20070512canon0251cs/ FIXED?
if BadResponse: Xxxx why
"""

## do not use Colname, do not use CommonName
def search_colname(request, colname, category="vascular"):
    version = VERSION
    print ("running search colname()", colname)
    names = Name.objects.filter(colnames__icontains=colname).exclude(upper__isnull=True).order_by("colnames")
    print ("found %s common names" % len(names))
    recs = []
    for name in names:
        if category == 'vascular':
            published = VascularImage.objects.filter(plant=name).filter(nr__gt=0).filter(nr__lt=100).count()
        else:
            return HttpResponseBadRequest("currently implemented for Vascular Plants only") ## FIXME
        try:
            rec = {"category": name.category, "spid": name.pk, "latname": "%s %s" % (name.upper.latname, name.latname),
                   "colnames": name.colnames, "published":published}
        except:
            print (name, name.category, "upper:", name.upper, name.latname)
            print (sys.exc_info())
            raise
        recs.append(rec)
        print (len(recs), rec) 
    return render (request, "photodb/results_colnames.htm", locals())
    
                                         

## search in names only
def search_colname_old(request, colname,  format="html"):
    version = VERSION
    print ("running search colname()", colname, format)
    qr = CommonName.objects.filter(colname__icontains=colname).order_by("colname")
    print ("found %s common names" % len(qr))
    recs = []
    for r in qr:
        name = r.ref_name
        published = VascularImage.objects.filter(plant=name).filter(nr__gt=0).filter(nr__lt=100).count()
        try:
            rec = {"category": name.category, "spid": name.pk, "latname": "%s %s" % (name.upper.latname, name.latname), "colnames": name.colnames, "published":published}
        except:
            print (r)
            print (sys.exc_info())
            try:
                rec = {"category": name.category, "spid": name.pk, "latname": "%s %s" % (name.legacy_parent.latname, name.latname),
                       "colnames": name.colnames, "published":published}
            except:
                raise
        recs.append(rec)
        print (len(recs), rec) 
    if format == "json":
        json = str(recs)
        ## print (json)
        return HttpResponse(json, "application/json")
    elif format == "xml":
        dom = xml.dom.minidom.parseString("<records/>")
        for r in recs:
            xrec = dom.createElement("record")
            for key in r:
                xrec.setAttribute(key, str(r[key]))
            print (xrec.toxml())
            ##print (dir(xrec))
            dom.documentElement.appendChild(xrec)
        return HttpResponse(dom.toxml(), "text/xml")
    elif format == "html":
        html = "<html><head></head><body><h1>Query Results (fast mode: all matched names with or without photos)</h1>"
        for r in recs:
            html += """<div><a href="/photodb/gallery/view/%s/">%s (%s)</div>""" % (r.get("spid", ""), 
                r.get("latname", ""), r.get("colnames", ""))
        html += "</body></html>"
        print (html)
        return render (request, "photodb/results_colnames.htm", locals())
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("format %s is not yet implemented" % format)

    return HttpResponse("XXX")

def get_tags(request):
    tags = {}
    for obj in (VascularImage, NonVascularImage, AnimalImage, VariaImage):
        table_name = obj._meta.object_name
        recs = obj.objects.exclude(tags__isnull=True).exclude(tags='')
        print (table_name, len(recs))
        for rec in recs:
            _tags = rec.tags.split(',')
            ## initially rec.imid, then rec.pk, then rec, but eventually enough (rec.pk, rec.spid, rec.imid)
            for _tag in _tags:
                if _tag in tags:
                    if tags[_tag].get(table_name):
                        tags[_tag][table_name].append(rec)
                    else:
                        tags[_tag] = {table_name:[rec]}
                else:
                    tags[_tag] = {table_name:[rec]}
        print (table_name, "tags", len(tags))
    print ("total", len(tags))
    html = "<html><head></head><body><h2>Total %s tags</h2><ol>\n" % len(tags)
    for tag in tags:
        html += "<li>%s %s</li>" % (tag, tags[tag])
    html += "</ol></body></html>"
    return render (request, "photodb/get_tags.htm", locals())

## difficult to  avoid index if using longname
##def search_latname(request, latname):
##    version = VERSION
##    names = Name.objects.filter(name__icontains=latname).order_by("latname")
##    photos = 0
##    for rec in names:
##        photos += rec.images
##        if rec.spid == 11886:
##            print ("debug:")
##            print (rec, "images", rec.images)
##    print ("search_latname for %s finished" % latname)
##    return render(request, "photodb/results_names.htm", locals())



def search_latname(request, latname):
    ## too difficult without filled LongName
    ##names = Name4.objects.filter(latname
    version = VERSION
    names = NameIndex.objects.filter(name__icontains=latname).order_by("name")
    photos = 0
    pubphotos = 0
    for rec in names:
         photos += rec.images
         pubphotos += rec.pubimages
    print ("search_latname for %s finished" % latname)
    return render(request, "photodb/results_names.htm", locals())
##    return HttpResponse(html)   
##    return HttpResponse("stub: %s" % str(names))

#### outdated
##def search_flag(request, flag):
##    ## domestic, cultivated, exotic
##    updated = None ## will be set to current time when running update Index
##    version = VERSION
##    photos = 0
##    if flag == "invasive":
##        meta_recs = SpeciesMeta.objects.exclude(invasive__isnull=True).exclude(invasive="").order_by("initial_name") ## FIXME initial_name
##    else:
##        meta_recs = SpeciesMeta.objects.filter(introduced=flag).order_by("initial_name") ## FIXME initial_name
##    print ("found", flag, len(meta_recs), "recs in meta")    
##    html = "<html><head></head><body><h1>Prototype using meta table: searching by flag [%s]: %s names found</h1><ol>\n" % (flag, len(meta_recs))
##    for meta in meta_recs:
##        try:
##            index_rec = NameIndex.objects.filter(spid=meta.spid)[0] ## in the index spid is not unique
##            meta.long_name = index_rec.long_name
##            meta.images = index_rec.images
##            photos += index_rec.images
##        except:
##            print ("no %s [%s] in NameIndex" % (meta.spid, meta.initial_name))
##            if not updated:
##                print ("will try to run debugging.name_index_update(None, delete=False)")
##                from . import debugging
##                updated = debugging.name_index_update(None, False) ## as datetime.datetetime.now() FIXME
##                print ("update index was called due to missing %s [%s] in NameIndex" % (meta.spid, meta.initial_name))
##            else:
##                print ("index was already updated: %s" % updated)
##            ## XXX : should now restart searching
##            meta.long_name = meta.initial_name
##            meta.images = 0
##            print (meta.__dict__)
##    return render(request, "photodb/results_flags.htm", locals())



INVASIVE_NOTES = { 7045:  ["/plants/invasive/notes/buddleja/"],
                   13992: ["/plants/invasive/notes/juniperus_conferta/"], ## not in our list
                   6510:  ["/plants/invasive/notes/20101024picea.html"],
                   12800: ["/plants/invasive/notes/20090809jasione.html"],
                   11330: ["/articles/atrocinerea2/", "/articles/atrocinerea/"],

    }



## new version :: in the field nonnative
updated = None
##from . import debugging ## needs to run update Index
def search_flag(request, flag, server="http://172.104.19.75"):
    global updated
    invasive_notes = INVASIVE_NOTES
    ##updated = None ## will be set to current time when running update Index
    version = VERSION
    photos = 0
    print ("running search2.search_flag for", flag)
    if flag == 'invasive':
        meta_recs = SpeciesMeta.objects.exclude(invasive__isnull=True).exclude(invasive="").order_by("initial_name") ## FIXME initial_name
        template = "photodb/results_flag_invasive.htm"
        print ("using invasive field")
    else:
        ##meta_recs = SpeciesMeta.objects.filter(nonnative=flag).order_by("initial_name") ## FIXME initial_name
        meta_recs = SpeciesMeta.objects.filter(introduced=flag).order_by("initial_name") ## FIXME initial_name
        print ("using old introduced field")
        template = "photodb/results_flags.htm"
    print ("found", flag, len(meta_recs), "recs in meta")    
    for meta in meta_recs:
        name = Name.objects.filter(pk=meta.pk)
        if not name:
            print (meta, "will skip due to error with meta without name")   ## 14850         
            continue
        else:
            name = name[0]
        if name.excluded:
            continue
        try:
            category = name.category
            meta.category = category
        except:
            images = VascularImage.objects.filter(pk=meta.pk).count()
            print (meta, "meta without name?", images, "images")            
            continue
        if flag == 'domestic':
            published = AnimalImage.objects.filter(plant=name).filter(nr__gt=0).filter(nr__lt=100).count()
        else:
            published = VascularImage.objects.filter(plant=name).filter(nr__gt=0).filter(nr__lt=100).count()
        meta.published = published
        try:
            index_rec = NameIndex.objects.filter(spid=meta.spid)[0] ## in the index spid is not unique
            meta.long_name = index_rec.long_name
            meta.images = index_rec.images
            photos += index_rec.images
        except:
            print ("no %s [%s] in NameIndex" % (meta.spid, meta.initial_name))
            if not updated:
                print ("will try to run debugging.name_index_update(None, delete=False)")
                updated = name_index_update(None, False) ## as datetime.datetetime.now() FIXME
                print ("update index was called due to missing %s [%s] in NameIndex" % (meta.spid, meta.initial_name))
            else:
                print ("index was already updated: %s" % updated)
            meta.long_name = meta.initial_name
            meta.images = 0
            print (meta.__dict__)
    print ("FIXME prototype: not well sorted, vascular and not plants together,run update because some without upper")
    return render(request, template, locals())


BUGS_TODO = """
Salix () (36 images) [http://localhost:9090/photodb/gallery/view/11886/] babylonica hybrids
    not in thums view !!!
    now http://localhost:9090/photodb/search/latname/Salix/ >> Salix () (36 images)  >> http://localhost:9090/photodb/gallery/view/11886/
    FIXED manually in Index file
    
Tree Salix fargesii () (11 images) [http://localhost:9090/photodb/gallery/view/17196/] >> 'NoneType' object has no attribute 'upper' [/media/data/data/django3/photodb/views.py, line 228, in thums_view_species ]
    i.e., in meta ?
    FIXED,
but  must have meta for all garden trees 

http://localhost:9090/photoDB/photos/gallery/11886/ without generic name
FIXED subgenus Salix but why used subgenus instead of genus 
FIXED and unsorted
"""
import pickle
def name_index_update(request, delete=False):
    start = datetime.datetime.now()
    print ("starting name_index_update, delete=", delete, "@", start)
    if delete:
        NameIndex.objects.all().delete()
        print ("cleaned index table")
    names = []
    unique = {}
    recs = Name.objects.filter(level='species') ## was Name4
    for r in recs:
        spid = r.pnid
        images = 0
        images += VascularImage.objects.filter(plant__pnid=spid).count()
        images += NonVascularImage.objects.filter(plant__pnid=spid).count()
        images += AnimalImage.objects.filter(plant__pnid=spid).count()
        images += VariaImage.objects.filter(plant__pnid=spid).count()
        latname = r.latname
        try:
           genname = r.upper.latname
        except:
           print ("cannot get upper.latname")
           try:
               genname = r.legacy_parent.latname
           except:
               print ("cannot get legacy parent.latname")
               genname = ""
        name = "%s %s" % (genname, latname)
        try:
           old_name = "%s %s" % (r.legacy_parent.latname, r.sal_latname)
        except:
           old_name = "XXX %s" % r.sal_latname
        if old_name == name:
            entry = {"spid": spid, "name": name, "classification": "both", "category": r.category}
            names.append(entry)
            unique[name] = spid
            if not delete and NameIndex.objects.filter(spid=spid): ## in idex spid explicit as a column
               ##print ("fast update mode skip", r)
               continue
            rec = NameIndex()
            rec.spid=spid
            rec.name = name
            rec.classification = "both"
            rec.category = r.category
            rec.images = images
            rec.long_name = "%s %s (%s)" % (name, r.authors, r.colnames)
            rec.save()            
        else:
            entry = {"spid": spid, "name": name, "classification": "new", "category": r.category}
            if not delete and NameIndex.objects.filter(spid=spid):
               ##print ("fast update mode skip", r)
               continue
            rec = NameIndex()
            rec.spid=spid
            rec.name = name
            rec.classification = "new"
            rec.category = r.category
            rec.images = images
            rec.long_name = "%s %s (%s)" % (name, r.authors, r.colnames)
            rec.save()
            unique[name] = spid
            names.append(entry)
            entry = {"spid": spid, "name": old_name, "classification": "old", "category": r.category}
            rec = NameIndex()
            rec.spid=spid
            rec.name = old_name
            rec.classification = "old"
            rec.category = r.category
            rec.images = images
            rec.long_name = "%s %s (%s)" % (old_name, r.sal_authors, r.colnames)
            rec.save()
            names.append(entry)
            unique[old_name] = spid
    if not delete:
        out = open("names.pickle", "wb")
        pickle.dump(names, out)
        out.close()
        print (len(names))
        out = open("names_unique.pickle", "wb")
        pickle.dump(unique, out)
        out.close()
        end = datetime.datetime.now()
        delta = end-start
        print (delta)
        print (len(unique))
    else:
       print ("update mode")
       end = datetime.datetime.now()
       delta = end-start
       print (delta)
    if request:
       return HttpResponse("updated index: %s seconds" % delta.seconds)
    else:
       return datetime.datetime.now()



