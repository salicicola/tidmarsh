import sys
from django.db.models import Q
from photodb.models import *
from inaturalist.models import *
from survey.models import *
from common.models import *
from names.models import *

def clean_vascular():
    bdcrecs = VascularImage.objects.exclude(Q(locality__pk__startswith="MA.BDC") | Q(locality__pk__startswith="MA.TDM"))
    print (len(bdcrecs))
    bdcrecs.delete()
    
def clean_varia():
    recs = VariaImage.objects.exclude(Q(locality__pk__startswith="MA.BDC") | Q(locality__pk__startswith="MA.TDM"))
    print (len(recs))
    recs.delete()

def clean_animals():
    recs = AnimalImage.objects.exclude(Q(locality__pk__startswith="MA.BDC") | Q(locality__pk__startswith="MA.TDM"))
    print (len(recs))
    recs.delete()

def clean_nonvascular():
    recs = NonVascularImage.objects.exclude(Q(locality__pk__startswith="MA.BDC") | Q(locality__pk__startswith="MA.TDM"))
    print (len(recs))
    recs.delete()

def clean_inaturalist():
    recs = InatRecord.objects.exclude(lcid="MA.TDM")
    print ("inat", len(recs))
    recs.delete()
    recs = ParsedLog.objects.all()
    print ("logs", len(recs))
    recs.delete()

## XXX restore and re-run :: towns, locations, generic
def clean_generic():
    recs = GenericRecord.objects.exclude(lcid__startswith="MA.TDM")
    print ("generic", len(recs))
    recs.delete()
    recs = GenericRecord.objects.filter(GUID__endswith="0000")
    print ("stub", len(recs))
    recs.delete()

def clean_common():
   recs = BugRecord.objects.all()
   print ("bugs", len(recs))
   recs.delete()
   recs = Town.objects.exclude(locID__startswith="MA.Plm")
   print ("towns", len(recs))
   recs.delete()
   recs = Location.objects.exclude(Q(lcid__startswith="MA.BDC") | Q(lcid__startswith="MA.TDM"))
   print ("locs", len(recs))
   recs.delete()

def clean_photos():
    recs = DeletedImage.objects.all()
    print ("deleted", len(recs))
    recs.delete()
    recs = FileRecord.objects.all()
    print ("files", len(recs))
    recs.delete()
    recs = ImagePublished.objects.all()
    print ("published", len(recs))
    recs.delete()
    recs = NameIndex.objects.all()
    print ("indexed", len(recs))
    recs.delete()
    recs = SpeciesPublished.objects.all()
    print ("spp published", len(recs))
    recs.delete()
	## left unouched :: Profiles, TidmarshRecord, Upload
    ## should recreate NameIndex

def clean_names():
    spids = {}
    for ob in [VascularImage, NonVascularImage, AnimalImage, VariaImage]:
        recs = ob.objects.all()
        for r in recs:
            spid = r.plant.pk
            if not spid in spids:
                spids[spid] = None
                print ("adding", spid, "total", len(spids))  ## 678 > 728
    recs = InatRecord.objects.all()
    for r in recs:
        try:
            spid = r.revised_name.pk
            if not spid in spids:
                spids[spid] = None
                print ("adding inat", spid, "total", len(spids))  ## 678 > 728
        except:
            print (sys.exc_info())
    recs = GenericRecord.objects.all()
    for r in recs:
        spid = r.plant.pk
        if not spid in spids:
            spids[spid] = None
            print ("adding generic", spid, "total", len(spids))  ## 678 > 728
    print ("total relevant spids", len(spids)) ## 744
    metarecs = SpeciesMeta.objects.all()
    for meta in metarecs:
        if meta.spid in spids:
            print ("existed", meta.spid)
            pass
        else:
            print ("may delete meta", meta)
    syns = Name.objects.filter(level='synonym')
    for syn in syns:
        par = syn.upper
        if par:
            if par.pk in spids:
                print ("existed species", par)
            else:
                print ("deleting syn", syn)
        else:
            print ("can delete synonym without species", syn)
    spp = Name.objects.filter(level='species')
    for sp in spp:
        if sp.pk in spids:
            print ("existed", sp)
        else:
            print ("deleting species", sp)
    genera = Name.objects.filter(level='genus')
    for gen in genera:
        spp = Name.objects.filter(upper=gen)
        print (gen, "with", len(spp), "species")
        if not spp:
            print ("may delete genus", gen)
    fams = Name.objects.filter(level='family')
    for fam in fams:
        genera = Name.objects.filter(upper=fam)
        print (fam, "with", len(genera), "genera")
        if not genera:
            print ("may delete family", fam)

def recreate_index():
    import photodb.debugging
    photodb.debugging.name_index_update(None)

import os, shutil
def copy_thums():
    missing = 0
    copied = 0
    for ob in [VascularImage, NonVascularImage, AnimalImage, VariaImage]:
        recs = ob.objects.all()
        for r in recs:
            src = "/media/data/data/tomcat/webapps/ROOT/thm/photos/%s/%s.jpg" % (r.imid[:6], r.imid)
            if os.path.exists(src):
                trgd = "data/static/thm/photos/%s" % r.imid[:6]
                if not os.path.exists(trgd):
                    os.mkdir(trgd)
                    print ("created", trgd)
                trg = "data/static/thm/photos/%s/%s.jpg" % (r.imid[:6], r.imid)
                if not os.path.exists(trg):
                    shutil.copy2(src, trg)
                    copied += 1
                    print ("copied", copied, r.imid)
            else:
                missing += 1
                print ("missing", missing, src)
## missing 1 /media/data/data/tomcat/webapps/ROOT/thm/photos/201804/20180422olymp0712cs.jpg
from urllib import request
import sys
def copy_photos(scaled=True):
    missing = 0
    copied = 0
    size = 0
    for ob in [VascularImage, NonVascularImage, AnimalImage, VariaImage]:
        recs = ob.objects.filter(nr__gt=0).filter(nr__lt=100)
        for r in recs:
            src = "/media/data/data/tomcat/webapps/ROOT/photos/%s/%s.jpg" % (r.imid[:6], r.imid)
            trgd = "data/static/photos/%s" % r.imid[:6]
            trg = "data/static/photos/%s/%s.jpg" % (r.imid[:6], r.imid)
            if not os.path.exists(trgd):
                os.mkdir(trgd)
                print ("created", trgd)
            if os.path.exists(src):                
                if not os.path.exists(trg):
                    shutil.copy2(src, trg)
                    copied += 1
                    size += os.path.getsize(trg)
                    print ("copied", copied, size, "total bytes", r.imid)
            else:
                missing += 1
                ##print ("missing", missing, src)
                url = "http://172.104.19.75/servlet/GetImage?id=r.imid"
                url = "http://172.104.19.75/static/photos/%s/%s.jpg" % (r.imid[:6], r.imid)
                print (url, trg)
                try:
                    request.urlretrieve(url, trg)
                    print ("retrieved", trg, os.path.getsize(trg))
                    ##break
                except:
                    print (sys.exc_info())
                    ##break
            ##break
    print ("total copied", copied, size/(1024*1024), "Mbs")
    print ("total missing", missing)






