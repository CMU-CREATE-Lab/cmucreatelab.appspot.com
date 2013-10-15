from controllers.users import user_required,BaseHandler
from google.appengine.ext import ndb
from models.warps import *
import webapp2
import json

class WarpHandler(BaseHandler):
    @user_required
    def post(self):
        warp = Warp(name = self.request.get('name'), description = self.request.get('description'), user_id = self.user.get_id(), location=self.request.get('location'))
        warp.put()
        self.redirect('/hyperwall/warps/%s' % warp.key.id())

    @user_required
    def put(self, warp_id):
        warp = Warp.get_by_id(int(warp_id))
        name = self.request.get('name', warp.name)
        description = self.request.get('description', warp.description)
        location = self.request.get('location', warp.location)
        warp.name = name
        warp.description = description
        warp.location = location
        warp.put()
        self.redirect('/hyperwall/warps/%s' % warp.key.id())

    @user_required
    def get(self, warp_id=None, extension=None):
        template_values = {}
        if warp_id:
            warp = Warp.get_by_id(int(warp_id))
            template_values['name'] = warp.name
            template_values['description'] = warp.description
        if extension == ".json":
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.write(json.dumps(warp.to_dict()))
        else:
            self.render_template('warp.html', template_values)


class WarpListHandler(BaseHandler):
    def get(self, extension=None):
        warps = Warp.query()
        template_values = { 'warps': warps }
        if extension == ".json":
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.write(json.dumps([(w.key.id(), w.to_dict()) for w in warps.fetch()]))
        else:
            self.render_template('warp_list.html', template_values)

class ListingListHandler(BaseHandler):
    def get(self, extension=None):
        listings = Listing.query()
        template_values = { 'listings': listings }
        if extension == ".json":
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.write(json.dumps([(l.key.id(), l.to_dict()) for l in listings.fetch()]))

class ListingHandler(BaseHandler):
    @user_required
    def post(self):
        objects = []
        if self.request.get('warp_ids'):
            ids = self.request.get('warp_ids').split(',')
            objects = ndb.get_multi([ndb.Key(Warp, int(k)) for k in ids])
            jsonObjects = json.dumps([(w.key.id(), w.to_dict()) for w in objects])
        listing = Listing(name = self.request.get('name'), objects = jsonObjects, user_id = self.user.get_id())
        listing.put()
        self.redirect('/hyperwall/listings/%s' % listing.key.id())

    @user_required
    def put(self, listing_id):
        listing = Listing.get_by_id(int(listing_id))
        name = self.request.get('name', listing.name)
        warp_ids = self.request.get('warp_ids', listing.warp_ids())
        ids = warp_ids.split(',')
        objects = ndb.get_multi([ndb.Key(Warp, int(k)) for k in ids])
        jsonObjects = json.dumps([(w.key.id(), w.to_dict()) for w in objects])        
        listing.name = name
        listing.objects = jsonObjects
        listing.put()
        self.redirect('/hyperwall/listings/%s' % listing.key.id())
        
    @user_required
    def get(self, listing_id=None, extension=None):
        template_values = {}
        if listing_id:
            listing = Listing.get_by_id(int(listing_id))
            template_values['name'] = listing.name
            template_values['warp_ids'] = listing.warp_ids()
        if extension == ".json":
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.write(json.dumps(listing.to_dict()))
        else:
            self.render_template('listing.html', template_values)
