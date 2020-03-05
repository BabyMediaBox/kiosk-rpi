# kiosk
The kiosk handles incoming http request send when the socket receives a command from the remote. 

## Implemented:
- Setting single RBG color
- Setting and RGB sequence that changes color after 2 seconds.
- Send to server when a button is pressed
- Load playlists for each button

# Requirements:
- tmux ( you can run without )
- nodejs 10+
- Browser - in kiosk mode or fullscreen without dialogs 
- [Running the BabyMediaBox server](https://github.com/BabyMediaBox/server)
- (Optional) The controller is rgb strips ( eyes of the robot in my instance ) [Running the BabyMediaBox arduino controller](https://github.com/BabyMediaBox/controller) 

# Running

Start your browser in kiosk mode and point it to the BabyBox server machine

For example
```
chromium-browser --kiosk http://BabyBoxServer:3010 &
python3 listen.py &
python3 input.py &
```

# tmux example script
```
#!/bin/bash

cd /home/pi/kiosk

SESSION_NAME="kiosk"


tmux new-session -s $SESSION_NAME -n "listen" -d 
tmux new-window -t $SESSION_NAME -n "input"
tmux new-window -t $SESSION_NAME -n "browser"

tmux send-keys -t $SESSION_NAME:1.1 'cd ~/kiosk; python3 listen.py' C-m
tmux send-keys -t $SESSION_NAME:2.1 'cd ~/kiosk; python3 input.py' C-m
tmux send-keys -t $SESSION_NAME:3.1 'chromium-browser --kiosk http://BabyBoxServer:3010' C-m
```  

# [![Demo](https://mraiur.com/files/BabyMediaBox.gif)](https://youtu.be/wDMkf0tSyG4)