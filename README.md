Simple tic tac toe game.

It is meant to be deployed to Google App Engine. It should be deployable with minimal if any changes. You will probably need to edit app.yaml with a new unique name in order to deploy it (after creating a new app in the Google developer dashboard for it).

To deploy, you will first need to download the App Engine SDK:

https://developers.google.com/appengine/downloads

Afterwards, create an application project for it here:

https://appengine.google.com/

Once you have done this, import the code into the App Engine SDK. Make sure that app.yaml contains the unique name for your application project, and not mine (extictactoe).

You should be able to deploy with one click.

A working demo is playable here: http://extictactoe.appspot.com/

My QA process for this software was relatively simple. I wrote the vast majority of the code inside a read, evaluate, print loop (REPL). When I was confident in my solution, I asked some friends to playtest for me. The first iteration of my AI proved to be beatable, so I researched and implemented a superior solution, whose pseudocode can be found here: http://en.wikipedia.org/wiki/Alpha-beta_pruning
