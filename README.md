# cybersec-educational-tools
This project contains a scoring engine for Ubuntu OS. The scoring engine checks to see if a student has caught certain vulnerabilities on the system and provides real-time feedback on student progress. For example, if the firewall is off, then the scoring engine will reward points to the student if they turn it back on. This allows students to gain hands-on experience at securing everything from web servers to standalone workstations. 

## How it works:
The teacher implements a list of vulnerabilities on a virtual machine and records them in engine.py, which will run every 30 seconds. As the student secures the system, the scoring engine will update Template.html to display a list of the vulnerabilites that the student caught correctly. The student is finished when they reach all 100 points or when the teacher calls time. 

#### Instructions

    on the desktop, create a file called "Set Name for Scoring Report" and inside, write the exact words YOUR FULL NAME: [id]
    mkdir /opt/temp and then copy cp_logo.jpeg, tts.jpg, engine.py, Template.html, time.txt into /opt/temp/ a) Make sure the permissions on /opt/temp and the contents inside are owned by the standard user that the competitor is intended to use(not root or anyone else). Make /opt/temp readable to that standard user: chmod u+r /opt/temp/* /opt/temp
    install python2 (yes this runs in python2 NOT python3), python-pip, git
    pip install requests (and any other libraries needed by engine.py)
    forensics questions are to be named in the following format: "/home/[username]/Desktop/Forensics_[#]” ex: /home/mando/Desktop/Forensics_1
    in engine.py, change the variables imageName, imageUserName to whatever you want
    note: for users who are intended to have poor passwords, create them using useradd instead of adduser ex: if points are to be awarded for changing the password of user bob, create the user bob using useradd rather than adduser
    note: AVOID USING SPACES IN ANY FILENAMES. ex: make a “this_is_a_vuln.mp3” instead of “this is a vuln.mp3”
    input any vulns using vulns.append([specific vuln]). The template provides an example of how to do this
    compile the code using pyconcrete or cython

pyconcrete guide: https://pypi.org/project/pyconcrete/
git clone <pyconcrete repo> <pyconcre dir>	
install pyconcrete
python setup.py install
pyconcrete-admin.py compile --source=/opt/temp --pye
pyconcrete engine.pye

    keep the .pye file, but remove the .py files (once everything is tested). From this point on, the way to run the scoring engine will be pyconcrete engine.pye
    create a service for the scoring engine (instructions below)
    run the engine at least once to create ScoringReport.html and then create a symlink (ln -s /opt/temp/ScoringReport.html /home/$USER/Desktop/ScoringReport.html)
    important: CLEAR HISTORY, create aliases in /root/.bashrc and /home/$USER/.bashrc with the line export HISTFILE=/dev/null
    also very important: REMOVE engine.py FROM THE ENTIRE SYSTEM (ex: make sure it's not in your trashbin). Would defeat the point of compiling everything if the competitor can find the decompiled version somewhere with all the vulns

#### Setting up the scoring engine

create file /lib/systemd/system/engine.service add below into it

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

#### Testing the scoring engine

    systemctl daemon-reload
    systemctl enable engine
    reboot
    systemctl status engine
