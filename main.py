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
import cgi
import json
import random
import webapp2
from google.appengine.api import memcache

MAIN_PAGE_HTML = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
    <head>
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <script type="text/javascript" src="script.js"></script>
        <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    </head>
    <body>
        <canvas id="square0" onclick="squareClicked(0, [KEY]);"></canvas>
        <canvas id="square1" onclick="squareClicked(1, [KEY]);"></canvas>
        <canvas id="square2" onclick="squareClicked(2, [KEY]);"></canvas>
        <br />
        <canvas id="square3" onclick="squareClicked(3, [KEY]);"></canvas>
        <canvas id="square4" onclick="squareClicked(4, [KEY]);"></canvas>
        <canvas id="square5" onclick="squareClicked(5, [KEY]);"></canvas>
        <br />
        <canvas id="square6" onclick="squareClicked(6, [KEY]);"></canvas>
        <canvas id="square7" onclick="squareClicked(7, [KEY]);"></canvas>
        <canvas id="square8" onclick="squareClicked(8, [KEY]);"></canvas>
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #generate a random number to use as the key for this game
        random.seed()
        game_key = random.randint(9999,99999)

        #insert the key into the HTML template
        html = MAIN_PAGE_HTML.replace('[KEY]', str(game_key))
        self.response.write(html)

class GetGameState(webapp2.RequestHandler):
    def get(self):
        return 0


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/gamestate', GetGameState)
], debug=True)
