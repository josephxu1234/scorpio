#authors: Joseph Xu, Gabriel Fok, Christos Bakis, Clement Chan, Jimmy Li
from subprocess import Popen
from tempfile import TemporaryFile
import json
import os
import sys
import getpass
import math
import itertools
import re
import subprocess
from time import gmtime, strftime, sleep, ctime
from datetime import datetime, date, timedelta
import requests
import json
import hashlib
import base64
import ast
import random
import string
import urllib

UNSCORED = 0
SCORED = 1
PENALTY = 2
INVALID = 3
currMinutes = 0
currHours = 0
runtime = "0:00"
#imageName is the name of the image itself; imageUserName is the name of the user that the competitor uses while doing the image. CASE MATTERS
imageName = "INSERT_NAME"
imageUserName = "INSERT_NAME"
namefile = open("/home/" + imageUserName + "/Desktop/Set Name for Scoring Report", "r")
name = namefile.readline()
name = name[16:-1]
namefile.close()
lastPoints = 0 
vulns = []


"""variables used by windows-edition scorpio implementation
honestly a lot of stuff needs cleaning but when i do clean something breaks soooo 
for example im not relying on the STARTTIME, UPDATETIME, TOTALTIME stuff at all and i'm just using my own time mechanism
but some of the remnants are still there :,(
just dont touch it lol
"""
NAME = name
IMAGE_NAME = imageName
STARTTIME = datetime.utcnow()
UPDATETIME = datetime.utcnow()
TOTALTIME = timedelta(0, 0, 0)

def sendscore(totalpoints, time):
    time = [x for x in time.split(":")][:2]
    if time[0][0] == '0' and len(time[0]) == 2:
        time[0] = time[0][1]
    #body = {"name": NAME, "imageName": IMAGE_NAME, "score": totalpoints, "totalTime": ":".join(time)}
    ##rewrite time mech
    body = {"name": NAME, "imageName": IMAGE_NAME, "score": totalpoints, "totalTime": runtime}
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post("http://cyber.jimmyli.us/api/user/addScore", data=json.dumps(body), headers=headers)
    except Exception as e:
        print("Error in sending score")
#stuff needed to work w scoring engine: 
def serversetup():
    global STARTTIME
    global UPDATETIME
    global TOTALTIME
    req = requests.get("http://cyber.jimmyli.us/api/user/getScores?name=" + urllib.pathname2url(NAME) + "&imageName=" + IMAGE_NAME)
    if req.content == b'[]':
        sendscore(0, "0:00:00")
    else:
        STARTTIME = datetime.strptime(ast.literal_eval(req.content.decode("utf-8"))[0]["startTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        UPDATETIME = datetime.strptime(ast.literal_eval(req.content.decode("utf-8"))[0]["updateTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        TOTALTIME = UPDATETIME - STARTTIME

def formattime(time):
    seconds = time.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    if seconds < 10:
        seconds = "0" + str(seconds)
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


class ConfigObject:
    path = ''
    key = ''
    entry = ''
    delim = ''
    keyFound = False
    points = 0
    comment = None

    def check(t):
        namefile = open("/home/sackboy/Desktop/Set Name for Scoring Report", "r") 
        name = namefile.readline()
        name = name[16:-1]
        namefile.close()
        if not t.path == '' and not t.key == '' and not t.entry == '' and not t.delim == '':
            f = open(t.path, 'r+')
            for line in f.readlines():
                checker = line.split(t.delim)
                t.keyFound = False
                for part in checker:
                    newPart = part.replace(' ', '')
                    newPart = newPart.replace('\n', '')
                    newPart = newPart.replace('\r', '')
                    t.keyFound = t.keyFound or newPart == t.key
                    if t.keyFound:
                        if newPart == t.entry:
                            f.close()
                            return (
                             1, t.points, t.comment)

            f.close()
            return (
             0, t.points, t.comment)
        print('Object not properly instantiated.')
        return (
         3, t.points, t.comment)


class UserObject:
    username = ''
    password = ''
    exist = None
    changePw = None
    correct = False
    points = 0
    comment = None

    def check(t):
        f = open('/etc/passwd', 'r+')
        if not t.exist == None:
            if t.exist:
                for userLine in f.readlines():
                    user = userLine.split(':')
                    if user[0] == t.username:
                        if t.changePw:
                            f.close()
                            f = open('/etc/shadow', 'r+')
                            for userLine in f.readlines():
                                user = userLine.split(':')
                                if user[0] == t.username and not user[1] == t.password:
                                    f.close()
                                    return (
                                     1, t.points, t.comment)

                            f.close()
                            return (
                             0, t.points, t.comment)
                        f.close()
                        return (
                         1, t.points, t.comment)

                f.close()
                return (
                 2, points, comment)
            for userLine in f.readlines():
                user = userLine.split(':')
                if user[0] == t.username:
                    f.close()
                    return (
                     0, t.points, t.comment)

            return (
             1, t.points, t.comment)
        else:
            for userLine in f.readlines():
                user = userLine.split(':')
                if user[0] == t.username:
                    f.close()
                    return (
                     1, t.points, t.comment)

            f.close()
            return (
             0, t.points, t.comment)
        return


class MemberObject:
    groupname = ''
    username = ''
    authorized = None
    points = 0
    comment = ''

    def check(t):
        if not t.authorized == None:
            f = open('/etc/group', 'r+')
            for groupLine in f.readlines():
                group = groupLine.split(':')
                if group[0] == t.groupname:
                    memberStr = group[3]
                    memberStr = memberStr.replace(' ', '')
                    memberStr = memberStr.replace('\r', '')
                    memberStr = memberStr.replace('\n', '')
                    memberList = memberStr.split(',')
                    if (memberList.count(t.username) > 0) == t.authorized:
                        f.close()
                        return (
                         1, t.points, t.comment)
                    f.close()
                    return (
                     0, t.points, t.comment)

            return (
             0, t.points, t.comment)
        return (
         3, t.points, t.comment)
        return


class CommandObject:
    command = ''
    output = ''
    expected = None
    points = 0
    comment = ''

    def check(t):
        if not t.expected == None:
            with TemporaryFile() as (output):
                cmd = Popen(t.command, stdout=output, shell=True)
                cmd.wait()
                output.seek(0)
                if (output.read().find(t.output) >= 0) == t.expected:
                    return (1, t.points, t.comment)
                return (
                 0, t.points, t.comment)
        else:
            return (
             3, t.points, t.commment)
        return

"""
String path = where the configuration file is located
String key = the specific configuration to be changed
String entry = the desired value of a certain configuration
int points: how many points this vuln is worth
String comment: the explanation that will show up on the scoring engine
"""
def newConfig(path, key, entry, delim, points, comment=''):
    confObj = ConfigObject()
    confObj.path = path
    confObj.key = key
    confObj.entry = entry
    confObj.delim = delim
    confObj.points = points
    confObj.comment = comment
    return confObj

"""
String username: the name of the user who is being checked
boolean exist: set to False to award points for removing a user; otherwise set to True for other configurations such as checking the existence of a password
boolean changePw: set to True to indicate that points will be awarded for setting a password; set to None for not applicable cases (ex: if the vuln is intended to check the removal of a user)
String password: set to "!" to indicate that points will be awarded for setting/changing a password, otherwise set to None
int points: how many points this vuln is worth
String comment: the explanation that will show up on the scoring engine

"""
def newUserObject(username, exist, changePw, password, points, comment=''):
    userObj = UserObject()
    userObj.username = username
    userObj.exist = exist
    userObj.changePw = changePw
    userObj.password = password
    userObj.points = points
    userObj.comment = comment
    return userObj

"""
String command: the command that will return some output to look through
String output: text to search for within the output of command
boolean expected: True means param output SHOULD be included within the output produced by param command
int points: how many points this vuln is worth
String comment: the explanation that will show up on the scoring engine

example: vulns.append(newCommandObject('cat "/home/sackboy/Desktop/Forensics Question 1"', 'Play! Create! Share! Huzzah!', True, 8, 'Forensics question 1 solved'))
will search for the existence (True) of Play! Create! Share! Huzzah! in the output of /home/sackboy/Desktop/Forensics Question 1 and award 8 points for correctness
"""
def newCommandObject(command, output, expected, points, comment=''):
    cmdObj = CommandObject()
    cmdObj.command = command
    cmdObj.output = output
    cmdObj.expected = expected
    cmdObj.points = points
    cmdObj.comment = comment
    return cmdObj


"""
int number: which forensics question is this? ex: Forensics 1
String answer: the expected answer
int points: the points to be awarded
"""
def forensics(number, answer, pts):
	cmdObj = newCommandObject("cat /home/" + imageUserName + "/Desktop/Forensics_" + str(number), answer, True, pts, "Forensics Question " + str(number) + " solved")
	return cmdObj


"""
String username: the name of the user to be removed
int points: the points to be awarded for removing that user
"""
def removedUser(username, pts):
	userObj = newUserObject(username, False, None, None, pts, 'Removed user ' + username)
	return userObj

def addedUser(username, pts):
	commandObj = newCommandObject("cat /etc/shadow", username, True, pts, "Added user " + username)
	return commandObj

def securedPassword(username, pts):
	userObj = newUserObject(username, True, True, '!', pts, 'Set a password for ' + username)
	return userObj

def removedSudoPriv(username, pts):
	commandObj = newCommandObject('sudo -l -U ' + username + ' | grep "not allowed"', 'not allowed', True, pts, username + ' is not an admin')
	return commandObj

def addedSudoPriv(username, pts):
	commandObj = newCommandObject('sudo -l -U ' + username + ' | grep "not allowed"', 'not allowed', False, pts, username + ' is an admin')
	return commandObj

def enabledFirewall(pts):
	commandObj = newCommandObject('ufw status', 'Status: active', True, pts, 'Firewall is enabled')
	return commandObj

"""
int port: the port that should be allowd
"""
def allowedPort(port, pts):
	commandObj = newCommandObject('ufw show added', 'allow ' + str(port), True, pts, 'Firewall allows port ' + str(port))
	return commandObj

def deniedPort(port, pts):
	commandObj = newCommandObject('ufw show added', 'deny ' + str(port), True, pts, 'Firewall denies port ' + str(port))
	return commandObj

"""
String filepath: location of configuration file
String key: the configuration to be changed
String value: what the configuration should be set to. If multiple values are used, it will be handled
ex: can pass "lcredit=-1", "ucredit=-1" as the values for *values
"""

def setConfig(filepath, key, points, *values):
	command = "grep -i " + key + " " + filepath
	valuesList = ""
	for value in values:
		command += " | grep -i " + value
		valuesList += value + ", "
	valuesList = valuesList[0:len(valuesList) - 2]
	commandObj = newCommandObject(command, key, True, points, key + ": " + valuesList + " config is set in " + filepath)
	return commandObj

"""
this specific method is used for configurations that can have a variety of values
ex: PASS_MAX_AGE 90 and PASS_MAX_AGE 30 are both acceptable if you set the threshold to 100 because 30, 90 <= 100
only works if key is in left most column (field), value is in column to the right of key
set lessThan to true if you want to check that the configured value is lessThan the threshold

int value
int threshold
boolean lessThan
"""
def setConfigInThreshold(filepath, key, points, threshold, lessThan):
	if lessThan:
		command = "if [ $(grep ^" + key + " /etc/login.defs | awk '{print $2}') -lt " + str(threshold) + ' ]; then echo "pointstime"; fi'
	else:
		command = "if [ $(grep ^" + key + " /etc/login.defs | awk '{print $2}') -gt " + str(threshold) + ' ]; then echo "pointstime"; fi'
	commandObj = newCommandObject(command, 'pointstime', True, points, key +" config is set with an appropriate value")
	return commandObj	
    
"""
String package: name of package that should be installed/removed
"""
def installedPkg(package, points):
	cmdObj = newCommandObject('apt list --installed | grep ^' + package + '/', 'installed', True, points, 'Software ' + package + 'installed')
	return cmdObj

def removedPkg(package, points):
	cmdObj = newCommandObject('apt list --installed | grep ^' + package + '/', 'installed', False, points, 'Prohibited software ' + package + ' removed')
	return cmdObj

"""
can use removedFile to check removal of a directory
ex: removedFile("/home/" , "prohibited.mp3", 3) checks for a prohibited.mp3 in /home
"""
def removedFile(directory, filepath, points):
	cmdObj = newCommandObject("ls " + directory, filepath, False, points, "removed prohibited file " + filepath)
	return cmdObj

"""
string version: the version that kernel should be greater than
"""
def updatedKernel(version, points):
	command = "if [ $(uname -r) != " + version + " ]; then echo pointstime; fi"
	cmdObj = newCommandObject(command, "pointstime", True, points, "updated kernel")
	return cmdObj
"""
string version: the version that firefox should be greater than
"""
def updatedFirefox(version, points):
	command = "if [ $(XAUTHORITY=/root/.Xauthority firefox -v | awk '{print $3}') != " + version + " ]; then echo pointstime; fi"
	cmdObj = newCommandObject(command, "pointstime", True, points, "updated Firefox")
	return cmdObj

"""
checks if the configuration within a file is removed/commented OR the file itself is gone
Good for files that are meant to be malicious. Bad for files that are required to be on the system
ex: you wouldn't want to award points for REMOVING /etc/ssh/sshd_config
String parentDir: the directory that contains file
String file: the config file itself
String config to check
int points: points to be awarded
"""
def removedConfigOrFile(filepath, config, points):
	command = "if [ ! -f " + filepath + " ] || ! grep -e '" + config + "' " + filepath + " || grep -e '" + config + "' " + filepath + " | grep -e '\s*#'; then echo pointstime; fi"
	cmdObj = newCommandObject(command, "pointstime", True, points, "removed malicious config in file " + filepath)
	return cmdObj

"""
checks if the configuration within a file is removed/commented
Good for files that are meant to remain on the system. ex: system configurations
"""
def removedOrCommentedConfig(filepath, config, points):
	command = "if ! grep -q '" + config + "' " + filepath + " || grep -e '" + config + "' " + filepath + " | grep -e '\s*#'; then echo pointstime; fi"
	cmdObj = newCommandObject(command, "pointstime", True, points, "removed malicious config in file " + filepath)
	return cmdObj

def writeScores(imageName, vulnLines, totalPoints, currentVulns, totalVulns):
    with open('/opt/temp/Template.html', 'r') as (input_file):
        with open('/opt/temp/ScoringReport.html', 'w') as (output_file):
            for line in input_file:
                if line.strip() == '{{LIST}}':
                    for vulnLine in vulnLines:
                        output_file.write(vulnLine)

                else:
                    newLine = line
                    newLine = newLine.replace('{{IMAGENAME}}', imageName)
                    newLine = newLine.replace('{{POINTS}}', str(totalPoints))
                    newLine = newLine.replace('{{CURRENT}}', str(currentVulns))
                    newLine = newLine.replace('{{VULNS}}', str(totalVulns))
                    newLine = newLine.replace('{{RUNTIME}}', runtime)
                    newLine = newLine.replace('{{NAME}}', name)
                    output_file.write(newLine)

def storeTime():
	f = open("/opt/temp/time.txt", "w")
	f.write(str(currHours) + "," + str(currMinutes))
	f.close()

def getTime():
	f = open("/opt/temp/time.txt", "r")
	time = f.read().rstrip().split(",")
	return (float(time[0]), float(time[1]))
######

def checkVuln(vuln):
    return vuln.check()

#PUT VULNS BELOW:
#ex: vulns.append(forensics(1, "What is autopilot?", 3))

def main():
    global currHours
    global currMinutes
    global runtime
    serversetup()
    while True:
        vulnLines = []
        totalPoints = 0
        currentVulns = 0
        tracker = 0
        for vuln in vulns:
            tracker += 1
            data = checkVuln(vuln)
            if data[0] == 1:
                totalPoints += data[1]
                currentVulns += 1
                vulnLines.append(data[2] + ' - ' + str(data[1]) + '<br>\n')

    
        lastPoints = totalPoints
        

        #new time mechanism
        time = getTime()
        currHours = time[0]
        currMinutes = time[1]

        runtime = "%d:%02d" % (currHours, int(math.floor(currMinutes)))
        writeScores(IMAGE_NAME, vulnLines, totalPoints, currentVulns, len(vulns))
        currMinutes += .5
        if currMinutes > 59:
            currMinutes = 0
            currHours += 1
        storeTime()

        if name != "<id>":
            req = requests.get("http://107.170.200.206/api/user/getScores?name=" + urllib.pathname2url(NAME) + "&imageName=" + IMAGE_NAME)
            UPDATETIME = datetime.strptime(ast.literal_eval(req.content.decode("utf-8"))[0]["updateTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
            TOTALTIME = UPDATETIME - STARTTIME
            sendscore(totalPoints, formattime(TOTALTIME))
            lastPoints = totalPoints
        sleep(30)
main()
