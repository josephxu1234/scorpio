# cybersec-educational-tools
This project contains a scoring engine for Ubuntu OS. The scoring engine checks to see if a student has caught certain vulnerabilities on the system and provides real-time feedback on student progress. For example, if the firewall is off, then the scoring engine will reward points to the student if they turn it back on. This allows students to gain hands-on projects at securing everything from web servers to standalone workstations. 

## how it works:
The teacher implements a list of vulnerabilities on a virtual machine and records them in engine.py, which will run every 30 seconds. As the student secures the system, the scoring engine will update Template.html to display a list of the vulnerabilites that the student caught correctly. The student is finished when they reach all 100 points or when the teacher calls time. 
