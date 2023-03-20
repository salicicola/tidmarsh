def get_authorized(request, perm="edit"): ## may have "rare|edit"
    if perm == 'rare':
        return False
    else:
        return True

VERSION = "#119 [21-09-28 : entry, edit (imported varia, animals]"
VERSION = "1.1.0 #120+ (2021-09-27T15:45:00)" ## use only here animals and varia
VERSION = "1.1.1 #127+ (2021-10-01T15:45:00)" ## names mini edit, login required"
VERSION = "1.1.2 (2021-10-07T10:15:00) #139+" ## front page & index page, cleaning
VERSION = "1.2.1 (2021-10-08T14:45:00) #144+" ## gimp only via tomcat, add image recs to other category... (~ as in bzr tags)
VERSION = "1.2.2 (2021-10-18T12:00:00) #163+" ## entry by dirs with minor bugs + using home~django prepare
VERSION = "1.2.3 (2021-10-27T11:15:00) #175+" ## many major changes
VERSION = "1.2.4 (2021-11-01T11:15:00) #190+" ## search module improved
VERSION = "1.2.5 (2021-11-05T21:30:00) #207+" ## added LegacyName
VERSION = "1.2.6 (2021-11-07) #208+" ## cleaning urls and front page, fixing bugs
VERSION = "1.2.7 (2021-11-08) #214+" ## added legacy checklist and clean Coronopus cases [recs in three tables for species and two recs for syns needed]
VERSION = "1.2.8 (2021-11-28) #231 last alpha" ## will remove negative ##, move 0000*.jpg, normalize
VERSION = "1.2.9 (2021-11-29) #241+ moving to beta" ## normalizing database
VERSION = "1.3.0 (2021-11-30) #244+ beta" ## tables normalized, backup kept, YET old PlantMeta and Name4 (to cnames)
VERSION = "1.3.1 (2021-11-30) #245+ beta" ##List view for families uses photodb AND generic records in survey module
### migrating to //beta/django3 restarting revno
VERSION = "1.3.2 (2021-12-01) #9+ beta" ## most important parts, ready to test at linode
VERSION = "1.3.2 (2021-12-09) #19+ beta" ## adding tidmarsh mapping from tidmarsh
VERSION = "1.3.3 (2021-12-13) #25+ beta" ## with Tidmarsh module (old URL only partially moved)
VERSION = "1.3.4 (2021-12-15) #42+ beta"  ## restored data entry with upload but only one file, and no edit form
VERSION = "1.3.5 (2021-12-18) beta"      ## #42+ uploading angain with authorization for testing
VERSION = "1.3.6 (2021-12-23) beta" ## added cached inaturalist draft with maps
VERSION = "1.4.0 (2022-01-12) #63+ beta" ## to linode + starts adding filtering for Tidmarsh
VERSION = "1.4.1 (2022-01-14) #64+ beta" ## to linode + starts adding filtering for Tidmarsh
VERSION = "1.4.2 (2022-01-18) #70+ beta" ## improved views, particularly Tidmarsh checklist
VERSION = "1.4.3 (2022-01-19) #75+ beta" ## essentially improving Tidmarsh checklist

