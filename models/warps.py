from google.appengine.ext import ndb
import json

class Warp(ndb.Model):
    user_id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    location = ndb.StringProperty()

class Listing(ndb.Model):
    user_id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    objects = ndb.JsonProperty()

    def warp_ids(self):
        objs = json.loads(self.objects)
        return ",".join([str(o[0]) for o in objs])

