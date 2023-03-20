import sys, os, socket ## os, sys not in use ?`
from django.conf import settings
from django.shortcuts import render ## _to_response  
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .models import VascularImage, TidmarshRecord
try:
    from survey.models import GenericRecord
except:
    from .models import GenericRecord
debug = True

def points_tidmarsh(spid):
    recs = TidmarshRecord.objects.filter(plant_id=spid)
    points = []
    for r in recs:
        imid = "TR: %s" % r.photo_url
        lat = r.lat
        lon = r.lon
        if not lat and not lon:
            coord = r.coordinates
            try:
                lat, lon = coord.split()
                lat = float(lat)
                lon = float(lon)
            except:
                print (sys.exc_info())
        notes = r.notes
        if lat and lon:
            points.append( (lon, lat, imid, notes) )
    print ("from explicit", spid, points)
    return points

def points_genericrecords(spid=2529):
    recs = GenericRecord.objects.filter(location__lcid__startswith='MA.TDM').filter(plant__pnid=int(spid))
    print (recs)
    points = []
    for r in recs:
        imid = "iNaturalist"
        latlon = r.gps
        notes = r.notes
        if latlon:
            try:
                lat, lon = latlon.split('-')
                lat = float(lat)
                lon = "-%s" % lon
                lon = float(lon)
                points.append( (lon, lat, imid, notes) )
            except:
                print ("error parsing latlon")
        return points

## extended MA.BDC.
def get_points(spid, lcid_starts):
    points = []
    recs = VascularImage.objects.filter(locality__lcid__startswith=lcid_starts).filter(plant__pnid=int(spid))
##    latname = recs[0].plant.latname
##    genname = recs[0].plant.upper.latname
##    latname = "%s %s" % (genname, latname)
    for r in recs:
        imid = r.imid
        latlon = r.gps
        notes = r.notes
        if latlon:
            try:
                lat, lon = latlon.split('-')
                lat = float(lat)
                lon = "-%s" % lon
                lon = float(lon)
                points.append( (lon, lat, imid, notes) )
            except:
                print ("cannot parse latlon", latlon)
    return points

def large_dot_map_new(request, spid, server="osm"):
    print ("start large_dot_mapper with param server =", server, "spid=", spid)
    print (socket.gethostbyname(socket.gethostname()))
    print (socket.getfqdn(socket.gethostbyname(socket.gethostname())))
    c = {}
    if socket.getfqdn(socket.gethostbyname(socket.gethostname())) == 'localhost':
        c["localhost"] = True
        print ("localhost True")
    else:
        c["localhost"] = False ## XXX
        print ("localhost false")
    if spid:
        points = []
        latname = colname = imid = ""
        recs = VascularImage.objects.filter(locality__lcid__startswith='MA.TDM').filter(plant__pnid=int(spid))
        if recs:
            latname = recs[0].plant.latname
            genname = recs[0].plant.upper.latname
            latname = "%s %s" % (genname, latname)
            for r in recs:
                imid = r.imid
                latlon = r.gps
                notes = r.notes
                print (latname, imid, latlon, notes)
                if latlon:
                    try:
                        lat, lon = latlon.split('-')
                        lat = float(lat)
                        lon = "-%s" % lon
                        lon = float(lon)
                        points.append( (lon, lat, imid, notes) )
                    except:
                        print ("cannot parse latlon", latlon)
        points_ext = get_points(spid, 'MA.BDC.')
        if points_ext:
            points.extend(points_ext)
        points_explicit = points_tidmarsh(spid)
        if points_explicit:
            points.extend(points_explicit)
        points2 = points_genericrecords(spid)
        if points2:
            points.extend(points2)
        c["points"] = points
        c["latname"] = latname
        c["colname"] = colname
        c["spid"] = spid
        c["debug"] = debug
        print (c)
        return render(request, 'tidmarsh2_large_dot_map.htm', c) ## plymouth_large_dot_map.htm tidmarsh_large_dot_map.htm exists
    else:
        return HttpResponseBadRequest("")
     
def large_dot_map_single(request, server="osm"):
    print ("large_dot_map_single", request.GET)
    c = {}
    points = []
    latname = request.GET.get("plantname", "")
    colname = request.GET.get("colname", "")
    spid = ""
    debug = ""
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    print ("lat", lat, "lon", lon, latname)
    if lat and lon:
        imid = ""
        notes = ""
        points.append( (lon, lat, imid, notes) )
    c["points"] = points
    c["latname"] = latname
    c["colname"] = colname
    c["spid"] = spid
    c["debug"] = debug
    print (c["points"])
    return render(request, 'tidmarsh2_large_dot_map.htm', c) ## plymouth_large_dot_map.htm tidmarsh_large_dot_map.htm exists
     
