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
'''
Tic Tac Toe - Human vs. Computer
I made the assumption that the human always plays first, and thus
the human is always "X". For the AI, I chose to use the alpha-beta
pruning variant of the Minimax algorithm after some brief research
on the subject. I used canvas tags to draw each square on the game
board, and the UI code communicates with the server via AJAX. The
state of a user's game is cached serverside using the memcache API
exposed by Google App Engine.

From a security standpoint: 
There is minimal verification of what is communicated between the 
client and server, and cheating at the game would be relatively trivial
for anyone who had even a basic knowledge of JavaScript. I did not
consider it very important for an application like this to have
strong input sanitization, but I do check the sanity of the key
in order to avoid the possibility for a buffer overflow. In the case
of a web application whose data is of a more sensitive nature, I would
use more thorough input sanitization, and likely force SSL. Theoretically, 
it is possible for one user to guess at the key of another user's game 
session and disrupt it, but the odds of doing so successfully are very slim.

Why is this code not object oriented?
I am perfectly comfortable writing OO Python, but for a project of this size
and scope, it would not really contribute anything except additional overhead. 
I understand and appreciate the advantages of writing OO code when working in
a team of developers - modularity and maintainability are paramount in that
sort of environment. For this application, I made a deliberate choice to keep
it simple. Where possible, I write functions without side effects, and since
Python does not have tail call optimization, I avoided recursion as much as
possible.
'''
import cgi
import json
import random
import moves
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
        <h2>Simple Tic Tac Toe vs. a Computer</h2>
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
        <br />
        <h3 id="announce">Click any square to begin.</h3>
    </body>
</html>
"""
#helper function to make sure that an invalid key is not passed
def sanitize_key(game_key):
    return 9999 < int(game_key) < 99999

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #generate a random number to use as the key for this game
        #Though the key space is relatively small, the chances of
        #a collision are low enough so as to be irrelevant for this
        #particular application.
        random.seed()
        game_key = random.randint(9999,99999)
        #initialize game board
        game_state = [False for i in range(9)]
        #cache initial game state
        memcache.add(key = str(game_key), value = json.dumps(game_state))
        #insert the key into the HTML template
        html = MAIN_PAGE_HTML.replace('[KEY]', str(game_key))
        #render the page
        self.response.write(html)

class GetGameState(webapp2.RequestHandler):
    def post(self):
        client = memcache.Client()
        game_key = self.request.get('key')
        #input sanitization
        if sanitize_key(game_key):
            #retrieve game state from cache
            try:
                game_state_json = client.gets(game_key)
                self.response.write(game_state_json)
            except:
                self.response.write(json.dumps([None for i in range(9)]))
        else:
            return 0
        
class UpdateGameState(webapp2.RequestHandler):
    def post(self):
        client = memcache.Client()
        game_key = self.request.get('key')
        game_state_json = self.request.get('game_state')
        #input sanitization
        if sanitize_key(game_key):
            try:
                game_state = json.loads(game_state_json)
                has_won = moves.winning_state(game_state)
                if has_won != False:
                    self.response.write(str(has_won))
                else:
                    #game is not over
                    game_state[moves.best_move(game_state)] = 'O'
                    #we have to check for a computer win again, rather than wait for another human move.
                    if moves.winning_state(game_state) == 2:
                        self.response.write("2")
                    else:
                        self.response.write("0")
                #update game state in cache
                memcache.set(key = game_key, value = json.dumps(game_state))
            except:
                self.response.write("0")
        else:
            return 0

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getgamestate', GetGameState),
    ('/updategamestate', UpdateGameState)
], debug=True)
