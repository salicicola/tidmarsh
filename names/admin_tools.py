from django.contrib import admin

from .models import *
from names.models import *

def set_upper_parent():
    recs = Name.objects.filter(upper__isnull=True).filter(parent__isnull=True)
    print (len(recs))
    for r in recs:
        legacy = r.legacy_parent
        if legacy:
            print (r, "?", r.parent, r.upper, legacy)
            r.upper = legacy
            r.parent = legacy
            print (r, "?", r.parent, r.upper, legacy)
            r.save()

names="Icteridae Anatidae Alcidae Ardeidae".split()
names="Accipitridae Cathartidae Cardinalidae Turdidae Tyrannidae Charadriidae".split()
names="Columbidae Picidae Corvidae Mimidae Gruidae Fringillidae Emberiridae Laridae Scolopacidae Meleagrididae Phalacrocoracidae Scolopacidae Passerellidae Paridae".split()
colnames = "Doves;Woodpeckers;Crows, Ravens, Jays, Rooks;Catbirds, Cowbirds, Mockingbirds;Cranes;Finches;American Sparrows, Juncos;Gulls, Terms, Skimmers;Sandpipers, Yellowlegs, Willets;Turkeys;Cormorants;Woodcocks;Towhees, Sparrows;Fitmice, Chickadees".split(';')
            
def add_actual_family(names=names, below=11950, category="animals"):
    parent = Name.objects.get(pnid=below)
    print ("parent/upper", parent)
    for i in range(len(names)):
    ##for name in names:
        name = names[i]
        ##colnames = colnames[i]
        r = Name()
        r.category = category
        r.rank = 'inter'
        r.actual_rank = "family"
        r.colnames = colnames[i]
        r.latname = name
        r.sal_latname = name
        r.parent = parent
        r.upper = parent
        r.legacy_parent = parent
        r.fid = parent.pnid
        r.colnames = ""
        r.save()
        print (r)
        
##def back_invasive():
##    recs = SpeciesMeta.objects.all()
##    for r in recs:
##        if r.invasive:
##            value = r.invasive
##            r.old_invasive = value
##            r.save()
##            print (r.pk, r.invasive, ">>", r.old_invasive, r.updated)

##def back_introduced():
##    recs = SpeciesMeta.objects.all()
##    for r in recs:
##        if r.introduced:
##            value = r.introduced
##            r.nonnative = value
##            r.save()
##            print (r.pk, r.introduced, ">>", r.nonnative, r.updated)

def set_introduced():
   recs = SpeciesMeta.objects.all()
   for r in recs:
       if r.invasive:
           print (r.invasive, "NN was", r.nonnative)
           r.nonnative = "invasive"
           r.save()
           print ("   >", r.nonnative, r.updated)
    
    
    
