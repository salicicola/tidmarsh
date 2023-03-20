from django.shortcuts import render ##_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import pickle, sys, os, datetime, time
##from settings import BASE
BASE = os.getcwd()
##print ("nogis_lib.BASE", BASE)
##XXX
try:
    _path = os.path.join(BASE, "data/pickle/names.pickle")
    names = pickle.load(open(_path, "rb"))
except:
    names = {}
    print ("DEBUG", sys.exc_info())
    raise
pickle_path = os.path.join(BASE, "data/pickle/gps_records.pickle")
data_modified = os.path.getmtime(pickle_path)

## NEW

try:
    gps_records = pickle.load(open(pickle_path, "rb"))
    ## list as ('42.27503', '-71.25956', '13381' {pnid}, '20131207ricoh8656cs', 72.0, 'MA.Nrf.Nee.2013120701', '12972')
    ## lat, lon, pnid, imid, nr, lcid, fid
except:
    gps_records = {}
    print (sys.exc_info())
    print ("should be list")
    raise

##print ("last modified/names/gps_records", data_modified, len(names), len(gps_records))
pickle_path = os.path.join(BASE, 'data/pickle/journal_gps_records.pickle')
data_modified = max(os.path.getmtime(pickle_path), data_modified)
try:
    _x = pickle.load(open(os.path.join(BASE, "data/pickle/journal_gps_records.pickle"), "rb"))
except:
    _x = {}
    print ("debug2", sys.exc_info())
##out = open("_x.txt", "w")
##out.write(str(_x))
##out.close()
pickle_path = os.path.join(BASE, "data/pickle/tdm_all.pickle")
data_modified = max(os.path.getmtime(pickle_path), data_modified)
##print "last_modified", data_modified
data_modified = datetime.datetime.fromtimestamp(data_modified)
print ("nogis_lib.data_modified", data_modified)
try:
    _y = pickle.load(open(os.path.join(BASE, "data/pickle/tdm_all.pickle"), "rb"))
except:
    _y = {}
    print (sys.exc_info())
##out = open("_y.txt", "w")
##out.write(str(_y))
##out.close()

##print len(_x), len(_y), "journal. tdm_all record"
_x.update(_y)
##print len(_x), "updated"
gps_tdm_records = _x
##print len(gps_tdm_records), "gps_tdm_records"
out = open("_updated.txt", "w")
out.write(str(gps_tdm_records))
out.close()

PARAMS = {"lat": 41.8560, "lon": -70.6760, "mapname":"flora_analyzer",
          "step": 800, "size": 800,  "width": 800,  "height": 800,
          "times": 10, "show_records":0, "direction": "WE", "method": "",
          "fname":"", "map_center_lon": -70.676, "map_center_lat": 41.856,
          "map_zoom": 12} 
##VERSION = "1.3.0 2018-04-07T12:00:00"
##print (__file__, "loading")

from .__init__ import VERSION


from .models import *
def get_gps_plantrecords():
    recs = VascularImage.objects.all()
    gps_records = []
    for r in recs:
        if r.gps:
            try:
                lat, lon = r.gps.split('-')
                lon = '-' + lon
                pnid = r.plant.pnid
                imid = r.imid
                fid = r.plant.legacy_parent.legacy_parent.pnid
                rec = (( lat, lon, pnid, imid, r.nr, r.locality.lcid, fid))
                print (rec)
                gps_records.append(rec)
            except:
                print (r.gps)
                print (sys.exc_info())
    print (len(gps_records), "total")
    print ("last", gps_records[-1])
    out = open("photodb/CACHE/gps_records.pickle", "wb")
    pickle.dump(gps_records, out)
    out.close()
## 49022 total
""" ma_tdm dict ::
'ind.2670.41.9014-70.57074':
    {'latname': 'Quercus velutina', 'colname': 'black oak', 'spid': '2670', 'lat': 41.9014,
    'imids': '20111022ricoh7181cs', 'unverified': False, 'inid': 'ind.2670.41.9014-70.57074',
    'lon': -70.57074, 'planted': False, 'lcid': 'MA.TDM.Ply.201110043', 'fid': '1444', 'nr': 60.0},
"""
def update_gps_records(pname='generic'):
    path = "photodb/CACHE/%s.pickle" % pname
    f = open(path, "rb")
    old = open("photodb/CACHE/gps_records.pickle", "rb")
    olddata = pickle.load(old)
    print ("old", len(olddata))
    newdata = pickle.load(f)
    print (newdata)
    for r in newdata:
        sp = Name.objects.get(pnid=int(r["spid"]))
        fid = sp.upper.upper.pnid
        rec = (( r["lat"], r["lon"], r["spid"], "", 0, r["lcid"], fid))
        print (rec)
        olddata.append(rec)
    print ("now", len(olddata))
    print ("last", olddata[-1])
    old.close()
    f.close()
    out = open("photodb/CACHE/gps_records.pickle", "wb")
    pickle.dump(olddata, out)
    out.close()
    print (out)

def update_gps_records_explicit():
    path = "photodb/CACHE/explicit.pickle"
    f = open(path, "rb")
    old = open("photodb/CACHE/gps_records.pickle", "rb")
    olddata = pickle.load(old)
    print ("old", len(olddata))
    newdata = pickle.load(f)
    print (newdata)
    for r in newdata:
        try:
            sp = Name.objects.get(pnid=int(r["spid"]))
            fid = sp.upper.upper.pnid
            if r.get("lat") and r.get("lon"):
                rec = (( r["lat"], r["lon"], int(r["spid"]), "", 0, r["lcid"], fid))
                print (rec)
                olddata.append(r)
            elif r.get("coordinates"):
                lat, lon = r.get("coordinates").split("-")
                lon = "-" + lon
                rec = (( lat, lon, int(r["spid"]), "", 0, r["lcid"], fid))
                print (rec)
                olddata.append(rec)
        except:
            ##print (sys.exc_info())
            pass
    print ("now", len(olddata))
    print ("last", olddata[-1])
    old.close()
    f.close()
    out = open("photodb/CACHE/gps_records.pickle", "wb")
    pickle.dump(olddata, out)
    out.close()
    print (out)
try:    
    from names.models import *
except:
    pass
from .models import *

def recreate_names_pickle():
    spp = {}
    names = Name.objects.filter(level="species").filter(category="vascular")
    for sp in names:
        try:
            longname = "%s %s" % (sp.legacy_parent.latname, sp.sal_latname)
            spid = str(sp.pnid)
            spp[spid] = longname
        except:
            print (sys.exc_info())
    print (len(spp), "total")            
    out = open("photodb/CACHE/names.pickle", "wb")
    pickle.dump(spp, out)
    out.close()
## 3721 total   

def recreate_tdm_all():
    recs = VascularImage.objects.filter(locality__lcid__startswith='MA.TDM')
    tdm_recs = {}
    for r in recs:
        if r.gps:
            inid = r.inid
            name = r.plant
            longname = "%s %s" % (name.legacy_parent.latname, name.sal_latname)
            lat, lon = r.gps.split('-')
            lon = '-' + lon
            planted = r.is_planted
            if not planted:
                planted = False
            else:
                if planted == 'yes':
                   print (planted)
                   planted = True
                print ("planted", planted)
            if r.is_verified:
                if r.is_verified == 'no':
                    unverified = True
                elif r.is_verified == 'yes':
                    unverified = False
                else:
                    raise Exception(r.is_verified)
            else:
                unverified = ""
            print ("unverified?", unverified)
            ##print (inid, name)
            if tdm_recs.get(inid):
                tdm_recs[inid]["imids"] += "," + r.imid
                ##print ("updated", tdm_recs[inid]["imids"]) ## checked : ,
            else:
                tdm_recs[inid] = {"latname": longname, "colname": name.colnames,
                              "spid": str(name.pnid), "lat": lat, "lon": lon,
                              "imids": r.imid, "unverified": unverified,
                              "inid": inid, "planted": planted, "nr": r.nr,
                              "lcid": r.locality.lcid,
                              "fid": name.legacy_parent.legacy_parent.pnid}
            ##print (tdm_recs[inid])
    print (len(tdm_recs))
    out = open("photodb/CACHE/tdm_all.pickle", "wb")
    pickle.dump(tdm_recs, out)
    out.close()
## 2833
## XXX unverified and planted

def explicit():
    recs = TidmarshRecord.objects.all()
    print ("explicit", recs)
    exp_recs = []
    for r in recs:
        rec = {"coordinates": r.coordinates, "lat": r.lat, "lon": r.lon, "lcid": r.lcid,
               "spid": r.plant_id, "name": r.plantname}
        print (rec)
        exp_recs.append(rec)
    print (len(exp_recs))
    out = open("photodb/CACHE/explicit.pickle", "wb")
    pickle.dump(exp_recs, out)
    out.close()

try:
    from survey.models import *
except:
    from .models import GenericRecord

## have Cabomba
def generic():
    recs = GenericRecord.objects.all()
   ## print ("generic", recs)
    generic = []
    for r in recs:
        if r.gps:
            lat, lon = r.gps.split('-')
            lon = '-' + lon
            rec = {"gps": r.gps, "lat": lat, "lon": lon, "lcid": r.lcid,
                   "spid": r.plant.pnid, "name": r.explicit_name}
            print (rec)
            generic.append(rec)
        else:
            print ("no coordinates", r)
    print (len(generic))
    out = open("photodb/CACHE/generic.pickle", "wb")
    pickle.dump(generic, out)
    out.close()

"""
dict:: journal_gps_records.pickle
'20150724olymp4030':
    {'inid': 'ind.13238.42.68481-71.9525', 'fid': '1503',
    'latname': 'Glyceria sp.', 'lon': -71.9525, 'lcid': 'MA.Wor.Asn',
    'spid': '13238', 'lat': 42.68481,
    'imids': '20150724olymp4030'},
## never more than one imid in imids
"""
##from journal.models import *
##def journal_pickle():
##    pass


def help_file(request, file_name="analyzer_help"):
    return render (request, file_name + '.htm', locals())

def get_all_params(request):
    ''' modified '''
    c = {}
    c["request_path"] = request.path
    for key in PARAMS.keys():
        default = PARAMS[key]
        value = request.GET.get(key, default) ## request.REQUEST.get(key, default) python 3 fixing
        ##print key, default, "from request", value
        if value:
            if type(value) == type(default) or type(default) == type(""):
                print ("OK")
            else:
                ##print "trying to eval value of ", key, "which value", value
                value = eval(value)
                ##print "casted to", value
            c[key] = value
        else:
            c[key] = default
        if c.get("show_records", None):
            c["points"] = get_all_dots()
            if c["points"]:
                c["total_photos"] = sum(c["points"].values()) 
                c["total_dots"] = len(c["points"])
            else:
                c["total_photos"] = 0 
                c["total_dots"] = 0          
    else:
        c["points"] = {}
    return c
## XXX : could not convert string to float: '41.5409.25'
## ONLY GPS records in use, not generic, not explicit
def _plants_box_count(lat, lon, width, height, found, boxes=[], run=1):
    center = (lon, lat)
    sofar = found.keys()
    newfinds = []
    box = (center[0] - (width/2.0) / (111111 * (373.0/500)),
         center[1] - (height/2.0) / 111111,
         center[0] + (width/2.0) / (111111 * (373.0/500)),
         center[1] + (height/2.0) / 111111)
    boxes.append(box)
    if not found:
        found = {}
    for photo in gps_records:
        try:
            _lat = float(photo[0])
            _lon = float(photo[1])
        except:
            print (sys.exc_info())
            ## FIXME
            continue
        spid = photo[2]
        if spid == 2529 or spid == '2529':
            if not photo[3]:
                print ("debug", photo)
        imid = photo[3]
        if _lat > box[1] and _lat < box[3]:
            if _lon > box[0] and _lon < box[2]:
                try:
                    try:
                        _latname = names[spid] ## was str
                    except:
                        _latname = names[str(spid)]
                    if spid in found: ## no has_key in python 3 found.has_key(spid)
                        runs = found[spid]["runs"]
                        if not run in runs:
                            runs.append(run)
                            ##print "ANOTHER FIND"
                    else:
                        runs = [run]
                    found[spid] = {'latname': _latname, 'lat':_lat, 'lon': _lon,
                                   'imids': imid, 'colname': '',
                                   'runs': runs}
                    if spid not in sofar:
                        newfinds.append(_latname)
                except:
                    print ("SHOULD NEVER HAPPEN, no latname for spid", spid)
                    print (sys.exc_info())
                    ##raise
    newfinds = set(newfinds)
    return (found, boxes, newfinds)

def get_all_dots():
    all_dots = {}
    for photo in gps_records: ## global
        _lat = float(photo[0])
        _lon = float(photo[1])
        lonlat = (_lon, _lat)
        if all_dots.has_key(lonlat):
            sofar = all_dots[lonlat]
            all_dots[lonlat] = sofar + 1
        else:
            all_dots[lonlat] = 1
##    print "unique dots", len(all_dots)
##    print "total photos", sum(all_dots.values())
    return all_dots

def get_species_from_found(found):
    all_species = []
    for key in found:
        latname = found[key]["latname"]
        runs = found[key]["runs"]
        if not latname in all_species:
            all_species.append((latname, runs, key))
    all_species.sort()
    return all_species    

def get_file_params(file_name):
    ''' cannot easily modify replacing size to width/height for now use ()'''
    if file_name:
        file_path = os.path.join(os.getcwd(), "transect_data", file_name)
        ##print file_path, os.path.exists(file_path)
        try:
            fname = open(file_path)
            _lonlats = []
            _width = None
            _height = None
            for line in fname:
                line = line.strip()
                if line and not line.startswith('#'):
                    x = eval(line)
                    if type(x) == type(0):
                        _size = x
                        ##print "found _size=", _size
                    elif type(x) == type((0,0)):
                        _lonlats.append(x)
                    else:
                        ##print "error parsing the file", file_path
                        ##print "line[", line, "]\n", x, type(x)
                        return ([], None, "Error parsing the file")
            fname.close()
            ##print "will return", len(_lonlats), "lonlats, tuple", (_size, _size)
            return (_lonlats, (_size, _size), None)
        except:
            ##print "File missing or corrupted"
            return ([], (None, None), "File missing or corrupted")
    else:
        ##print "No File name"
        return ([], (None, None), None)

def get_lonlats(request):
    ll = []
    if 'lonlats' in request.REQUEST:
        for xy in request.REQUEST['lonlats'].split(','):
            if xy.strip():
                _lon, _lat = xy.strip().split()
                coor = (float(_lon), float(_lat))
                ll.append(coor)
    return ll

def make_raw_lonlats(lonlats):
    s = ""
    for lon, lat in lonlats:
        s += "%s %s," % (lon, lat)
    return s

def get_transect_boxes(c, times, lat, lon, width, height):
    """ 1.1.14 2015-02-24T16:40:00 """
    found = {}
    counted = []
    boxes = []
    for i in range(times):
        (found, boxes, stub) = _plants_box_count(lat, lon, width, height, found, boxes, i+1)
        if c["direction"] == 'up' or c["direction"] == 'SN':                           
            lat = lat + c["height"]/111111.0                   
        elif c["direction"] == 'NS':
            lat = lat - c["height"]/111111.0
        elif c["direction"] == 'EW':
            lon = lon - c["width"]/ (111111 * (373.0/500)) 
        elif c["direction"] == 'right' or c["direction"] == 'WE':                                           
            lon = lon + c["width"]/ (111111 * (373.0/500))
        else:
            return HttpResponseBadRequest('bad direction "' + c["direction"] + '"')
        _counted = len(found)
        counted.append(_counted)
        ##size += step                              
    return (found, counted, boxes, stub)
##
##print ("loaded", __name__)

def recreate_pickle():
    get_gps_plantrecords()
    time.sleep(3)
    update_gps_records_explicit()
    time.sleep(3)
    update_gps_records(pname='generic')
    print ("all done")
