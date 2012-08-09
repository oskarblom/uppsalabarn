#!/bin/bash

cd /Users/oskar/Projects/uppsalabarn
workon uppsalabarnenv

tmux new-session -d -s uppsalabarn
tmux new-window -t uppsalabarn:1 -n "mongo" "startmongo"
tmux new-window -t uppsalabarn:2 -n "sass" "sass --watch site.scss:static/css/site.css"
