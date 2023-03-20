from django.db import models

class Name (models.Model):
    pnid = models.AutoField(primary_key=True)
##    ccss = models.IntegerField(null=True, blank=True) ## Integer was ## XXX , unique=True removed for now
    category = models.CharField(max_length=50, blank=True, default="vascular") ## 
    level = models.CharField(max_length=50, blank=True) ## group, etc = elementName , 
    rank = models.CharField(max_length=50, blank=True)
    latname = models.CharField(max_length=150, blank=True) ## sal name if not  = ccss
    authors = models.CharField(max_length=150, blank=True)
    colnames = models.CharField(max_length=150, blank=True) ##sal name
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    upper = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="Fid_Gid") ## 
    longname = models.CharField(max_length=250, blank=True)
    note = models.TextField(blank=True)
    caption = models.TextField(blank=True, default="")
    excluded = models.BooleanField(default=False)

    legacy = models.BooleanField(default=False, verbose_name="legacy only",
            help_text="if true, latname, authors, parent, upper fields to be left empty (use matched LegacyName record")
    legacy_parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="legacy_upper")
    fid = models.IntegerField(null=True, blank=True)
    sal_latname = models.CharField(max_length=150, blank=True) ## sal name if not  = ccss
    sal_authors = models.CharField(max_length=150, blank=True)
    ##sal_colnames = models.CharField(max_length=150, blank=True)
    disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return("%s: %s / %s" % (self.pnid, self.latname, self.sal_latname))

    class Meta:
        verbose_name_plural = 'NameRecords'

class LegacyName(Name):
    class Meta:
        proxy = True

class CommonName(models.Model):
    ref_name = models.ForeignKey(Name, on_delete=models.RESTRICT)
    colname = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return("%s: %s [%s]" % (self.ref_name.latname, self.colname, self.created))

    class Meta:
        unique_together = ('ref_name', 'colname')
    
class NameMini(Name):

    class Meta:
        proxy = True
        verbose_name_plural = 'NamesPart'

class SpeciesMeta (models.Model):
    spid = models.IntegerField(primary_key=True) ## == pnid or ccss ???
    evergreen=models.CharField(max_length=150, blank=True)
    introduced=models.CharField(max_length=150, blank=True, verbose_name="NonNative")
    ##nonnative=models.CharField(max_length=150, blank=True, default="", verbose_name="NewNonNative")
    invasive_mipag=models.CharField(max_length=150, blank=True)
    invasive=models.CharField(max_length=150, default="", blank=True)
    origin=models.CharField(max_length=150, blank=True)
    rare=models.CharField(max_length=150, blank=True)
    updated=models.DateTimeField(auto_now=True)
    ## from CCSS
    counties=models.CharField(max_length=150, blank=True, default="* * * * * * * * * * * * * *")
    counties_changed_from = models.CharField(max_length=150, blank=True)
    status=models.CharField(max_length=150, blank=True)
    su_ba=models.CharField(max_length=150, blank=True, default="yes")
    ## in <status id="20925" invasive="likely">SNA</status>

    initial_name = models.CharField(max_length=150, blank=True)
    rank = models.CharField(max_length=150, blank=True, default="species")
    
    def __str__(self):
        return str(self.spid)
    class Meta:
        verbose_name_plural = 'SpeciesMeta'
