import sys, os, socket, datetime ##, timezone ## os, sys not in use ?`
from django.conf import settings
from django.shortcuts import render ## _to_response  
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .models import * ## VascularImage, TidmarshRecord
try:
    from survey.models import GenericRecord
    from names.models import Name, SpeciesMeta
    from inaturalist.models import InatRecord
except:
    print ("should already imported from .", Name, SpeciesMeta, GenericRecord)

import xml.dom.minidom
def import_xml_notes():
    dom = xml.dom.minidom.parse("photodb/tidmarsh/XML/notes.xml")
    print (dom)
    for note in dom.getElementsByTagName("note"):
        spid = int(note.getAttribute("spid"))
        plant = Name.objects.get(pk=spid)
        text = note.firstChild.nodeValue
        text = text.strip()
        rec = ChecklistNote()
        rec.plant = plant
        rec.note = text
        rec.save()
        print (rec.plant, rec.note, rec.modified)
    for note in dom.getElementsByTagName("comment"):
        spid = int(note.getAttribute("spid"))
        plant = Name.objects.get(pk=spid)
        text = note.firstChild.nodeValue
        text = text.strip()
        rec = ChecklistNote()
        rec.plant = plant
        rec.comments = text
        rec.save()
        print (rec.plant, rec.comments, rec.modified)

def import_xml_old():
    dom = xml.dom.minidom.parse("photodb/tidmarsh/XML/old_notes.xml")
    print (dom)
    for note in dom.getElementsByTagName("r"):
        spid = int(note.getAttribute("spid"))
        plant = Name.objects.get(pk=spid)
        try:
            text = ""
            for child in note.childNodes:
                if child.nodeType == note.TEXT_NODE:
                    text += child.nodeValue                   
            ##text = note.firstChild.nodeValue
            text = text.strip()           
            if text:
                existed = ChecklistNote.objects.filter(plant=plant).filter(checklist='Tidmarsh')
                if existed:
                    rec = existed[0]
                    old = rec.note
                    if old:
                        rec.note = text + " [" + text + "]"
                    else:
                        rec.note = "[" + text + "]"
                    rec.modified = datetime.datetime(2018, 4, 16)
                    rec.save()
                else:
                    rec = ChecklistNote()
                    rec.plant = plant
                    rec.note = "[" + text + "]"
                    rec.save()
                print ("saved", rec.plant, rec.note, rec.modified)
        except:
            print (sys.exc_info())
            


        
def edit_note(request, spid):
    plant = Name.objects.get(pk=int(spid))
    note = ChecklistNote.objects.filter(checklist='Tidmarsh').filter(plant=plant)[0]
    url = "http://192.168.1.9:9090/admin/photodb/checklistnote/%s/change/" % note.pk
    print ("redirecting to %s" % url)
    return HttpResponseRedirect(url)

## recreating page   
def create_tdm_inat(request, template="photodb/tidmarsh/make_inatrecs.htm"):
    recs = GenericRecord.objects.filter(location__pk__startswith='MA.TDM').filter(GUID__startswith="https://www.inaturalist.org/")
    recs = recs.exclude(gps_error__contains='km')
    print (len(recs)) 
    spp = {}
    try:
        total_recs = InatRecord.objects.filter(notes='Tidmarsh Bounding Box').count()
        totals = InatRecord.objects.filter(lcid='MA.TDM').count() ## FIXME not equal
    except:
        raise Exception("running at the server without iNat records")
    for r in recs:
        if r.plant: 
            plant = r.plant
            try:
                gname = plant.upper.latname
            except:
                gname = "XXX"            
            lname = plant.latname
            spid = plant.pk
            ## extremely bad design FIXME
            photos = VascularImage.objects.filter(plant=plant).filter(locality__pk__startswith='MA.TDM').count()
            key = ((gname, lname, spid, photos))
            gps = r.gps
            if gps and ' ' in gps.strip():
                lat, lon = gps.strip().split()
                r.lat = lat
                r.lon = lon
                err = r.gps_error
                if err == 'Not recorded':
                    r.gps_error = ''
            if key in spp:
                spp[key].append(r)
            else:
                spp[key] = [r]
        else:
            print ("ERROR", r)    
    print (len(spp), "species") 
    plants = spp.items()
    plants = list(plants)
    plants.sort()
    generated = timezone.now()
    return render (request, template, locals())

    
                                        
    
