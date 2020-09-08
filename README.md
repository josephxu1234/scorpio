# Scorpio-Scoring-Engine-for-Ubuntu
Scores ubuntu VMs for CyberPatriot practice
Created by: Joseph Xu, Gabriel Fok, Christos Bakis, Clement Chan, Jimmy Li

#####instructions######
1) on the desktop, create a file called "Set Name for Scoring Report" and inside, write the exact words YOUR FULL NAME: [id]
2) mkdir /opt/temp and then copy cp_logo.jpeg, tts.jpg, engine.py, Template.html, time.txt into /opt/temp/
	a) Make sure the permissions on /opt/temp and the contents inside are owned by the standard user that the competitor is intended to use(not root or anyone else). Make /opt/temp readable to that standard user: chmod u+r /opt/temp/* /opt/temp
3) install python2 (yes this runs in python2 NOT python3), python-pip, git
4) pip install requests (and any other libraries needed by engine.py)
5) forensics questions are to be named in the following format: "/home/[username]/Desktop/Forensics_[#]”
	ex: /home/mando/Desktop/Forensics_1 
6) in engine.py, change the variables imageName, imageUserName to whatever you want
7) note: for users who are intended to have poor passwords, create them using useradd instead of adduser
ex: if points are to be awarded for changing the password of user bob, create the user bob using useradd rather than adduser
8) note: AVOID USING SPACES IN ANY FILENAMES. 
	ex: make a “this_is_a_vuln.mp3” instead of “this is a vuln.mp3”
9) input any vulns using vulns.append([specific vuln]). The template provides an example of how to do this
10) compile the code using pyconcrete or cython
```
pyconcrete guide: https://pypi.org/project/pyconcrete/
git clone <pyconcrete repo> <pyconcre dir>	
install pyconcrete
python setup.py install
pyconcrete-admin.py compile --source=/opt/temp --pye
pyconcrete engine.pye
```

11) keep the .pye file, but remove the .py files (once everything is tested). From this point on, the way to run the scoring engine will be pyconcrete engine.pye
12) create a service for the scoring engine (instructions below)
13) run the engine at least once to create ScoringReport.html and then create a symlink (ln -s /opt/temp/ScoringReport.html /home/$USER/Desktop/ScoringReport.html)
14) important: CLEAR HISTORY, create aliases in /root/.bashrc and /home/$USER/.bashrc with the line export HISTFILE=/dev/null
15) also very important: REMOVE engine.py FROM THE ENTIRE SYSTEM (ex: make sure it's not in your trashbin). Would defeat the point of compiling everything if the competitor can find the decompiled version somewhere with all the vulns

#####Setting up the scoring engine#####

create file /lib/systemd/system/engine.service
add below into it 
```
[Unit]
Description=Scoring Engine
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=(path to pyconcrete cmd) /opt/temp/engine.pye

[Install]
WantedBy=multi-user.target
```
#####testing the scoring engine#####
1) systemctl daemon-reload
2) systemctl enable engine
3) reboot
4) systemctl status engine
