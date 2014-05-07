Simple tic tac toe game.

It is meant to be deployed to Google App Engine. It should be deployable with minimal if any changes. You will probably need to edit app.yaml with a new unique name in order to deploy it (after creating a new app in the Google developer dashboard for it).

A working demo is playable here: http://extictactoe.appspot.com/

My QA process for this software was relatively simple. I wrote the vast majority of the code inside a read, evaluate, print loop (REPL). When I was confident in my solution, I asked some friends to playtest for me. The first iteration of my AI proved to be beatable, so I researched and implemented a superior solution, whose pseudocode can be found here: http://en.wikipedia.org/wiki/Alpha-beta_pruning