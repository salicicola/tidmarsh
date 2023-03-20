from django.db import models
from common.models import Location
from names.models import Name

class GenericRecord(models.Model):
    GUID = models.CharField(max_length=255, primary_key=True) ## made primary
    plant =  models.ForeignKey(Name, null=True, blank=True, on_delete=models.SET_NULL) ## modified to Name4
    explicit_name = models.CharField(max_length=150, null=True, blank=True)
    lcid = models.CharField(max_length=150, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    explicit_location =  models.CharField(max_length=150, null=True, blank=True) ## +
    town = models.CharField(max_length=150, null=True, blank=True) ## +
    date = models.CharField(max_length=150, null=True, blank=True) ## +
    gps = models.CharField(max_length=150, null=True, blank=True)
    gps_error = models.CharField(max_length=10, null=True, blank=True) ## irrelevant ?
    source = models.CharField(max_length=255, default="salicicola:plantgallery")  ## salicicola.survey
    notes = models.CharField(max_length=255, blank=True, null=True)
    kind = models.CharField(max_length=10, choices=(("add", ""), ("del", "del")), default="")
    committed = models.DateTimeField(null=True, blank=True) ## XXX: to change name: taken from file timestamp
    modified = models.DateTimeField(null=True, blank=True) ## auto_now=True

    def __str__(self):
        return "%s" % self.GUID

 
