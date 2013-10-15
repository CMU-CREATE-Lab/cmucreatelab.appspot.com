#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from controllers import users,warps

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.users.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR SECRET KEY'  
  }
}

# Deploy with a "real" secret_key

app = webapp2.WSGIApplication([
        webapp2.Route('/', MainHandler, name='home'),
        webapp2.Route('/login', users.LoginHandler, name='login'),
        webapp2.Route('/signup', users.SignupHandler, name='signup'),
        webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
                      handler=users.VerificationHandler, name='verification'),
        webapp2.Route('/password', users.SetPasswordHandler),
        webapp2.Route('/logout', users.LogoutHandler, name='logout'),
        webapp2.Route('/forgot', users.ForgotPasswordHandler, name='forgot'),
        webapp2.Route('/authenticated', users.AuthenticatedHandler, name='authenticated'),

        webapp2.Route('/hyperwall/warps', warps.WarpHandler, name='warp'),


        webapp2.Route('/hyperwall/warps/<warp_id:\d+>', warps.WarpHandler, name='warp'),
        webapp2.Route('/hyperwall/warps/<warp_id:\d+><extension:.json>', warps.WarpHandler, name='warp'),
        webapp2.Route('/hyperwall/warps', warps.WarpListHandler, name='warp'),
        webapp2.Route('/hyperwall/warps<extension:.json>', warps.WarpListHandler, name='warp'),

        webapp2.Route('/hyperwall/listings', warps.ListingListHandler, name='list'),
        webapp2.Route('/hyperwall/listings<extension:.json>', warps.ListingListHandler, name='list'),

        webapp2.Route('/hyperwall/listings/<listing_id:\d+>', warps.ListingHandler, name='list'),
        webapp2.Route('/hyperwall/listings/<listing_id:\d+><extension:.json>', warps.ListingHandler, name='list'),       ], 
                              config=config,
                              debug=True)

