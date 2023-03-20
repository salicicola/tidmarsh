from django.db import models
from django.utils import timezone
from names.models import Name

class InatRecord(models.Model):
    inat_id = models.CharField(max_length=250, primary_key=True)
    GUID = models.URLField(max_length=250, null=True) ## url
    taxon_id = models.IntegerField(null=True, blank=True)
    latname = models.CharField(max_length=250, default="", null=True, blank=True)
    comname = models.CharField(max_length=250, default="", null=True, blank=True)
    revised_name = models.ForeignKey(Name, null=True, blank=True, on_delete=models.SET_NULL)
    revised_by = models.CharField(max_length=10, default="", null=True, blank=True)
    revised_data = models.DateField(null=True, blank=True, default=None)
    revised_note = models.CharField(max_length=250, null=True, blank=True, default="")
    planted = models.BooleanField(default=False)
    urban = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default="", blank=True, null=True)
    saved_in = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True, default="")
    lcid =  models.CharField(max_length=250, null=True, blank=True, default="MA.TDM") ## FIXME
    notes = models.CharField(max_length=250, null=True, blank=True, default="")
    observed = models.DateTimeField(null=True, blank=True)
    observer = models.CharField(max_length=250, null=True, blank=True, default="", verbose_name="user")
    latlon = models.CharField(max_length=250, null=True, blank=True, default="")
    accuracy = models.CharField(max_length=250, null=True, blank=True, default="")
    gps_error = models.IntegerField(null=True, blank=True)
    approved = models.IntegerField(default=0, choices=[(i, i) for i in range(-1, 3)]) ## -1 notidentifiable, 0: no ids, 1-3: matched ids, i.e., if < 2 needs ID
    verbose_date = models.CharField(max_length=250, null=True, blank=True, default="")
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modified = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__ (self):
        return "%s [%s]" % (self.comname, self.location)

class ParsedLog(models.Model):
    inID = models.IntegerField(primary_key=True) ## taxon_id
    pnid = models.IntegerField(null=True)    
    records = models.IntegerField(default=0)
    parsed = models.DateField(null=True)

    def __str__ (self):
        return "%s = salicicola %s (%s recs last checked %s" % (self.inID, self.pnid, self.records, self.parsed)


