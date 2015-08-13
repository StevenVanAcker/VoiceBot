#!/usr/bin/env python
# coding: latin-1
# dr_root 2011

# Edited by lidbjork, january 2013

# vol was here, september 2013 osv

import socket
import os
import sys
import random
import time
import getopt


### Send OK message to daemon

def ok(sock):
	d = sock.recv(128)
	if d.strip() != "OK":
		print d.strip()
		sys.exit(-1)
	return True	


### Connect to daemon

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(10.0)
	s.connect(("tw.cracksucht.de",7600))
	if s.recv(128).strip() != "KAKRAFOON2":
		print "Incorrect daemon"
		sys.exit(0)
	return s


### Send audio file or stream URL to daemon

def sendfile(file):
	if "youtube" or "youtu.be" in file:
		file = file.replace("youtu.be/", "www.youtube.com/watch?v=")  # unshorten url if shortened
		file = file.replace("https://", "http://")  # https is okay but will be replaced with http !
	stream = ("http://" in file) or ("https://" in file)
	if not stream and not os.path.isfile(file):
		print "%r is not a file. Skipping" % file
		return

	if not stream: print "Queueing %r.." % file.split("/")[-1]
	else: print "Queueing %r.." % file
#	print "Filesize: %r" % filesize
	s = connect()
	s.sendall("ADD\n")
	ok(s)
	if not stream:
		s.sendall(file.split("/")[-1])
		ok(s)
		filesize = os.path.getsize(file)
		s.sendall(str(filesize))
		ok(s)
		s.sendall(open(file,"rb").read())
		s.close()
	else:
		s.sendall(file)
		ok(s)


### Show queue in classic format with filenames/urls

def queue():
	s = connect()
	s.sendall("SHOWQUEUE\n")
	length = int(s.recv(4),16)
	print s.recv(length,socket.MSG_WAITALL)
	sys.exit(0)


### Show queue in "human readable" format

def queuehuman():
	s = connect()
	s.sendall("SHOWLONG\n")
	length = int(s.recv(4),16)
	print s.recv(length,socket.MSG_WAITALL)
	sys.exit(0)


### Remove song from queue

def remove(jobid):
	s = connect()
	s.sendall("REMOVE\n")
	ok(s)
	s.sendall(jobid)
	ok(s)
	sys.exit(0)


def time_to_seconds(t):
	time=0
	ht=t.split('h', 1)
	try:
		t=ht[1]
		time+=int(ht[0])*3600
	except:
		pass
	mt=t.split('m', 1)
	try:
		t=mt[1]
		time+=int(mt[0])*60
	except:
		pass
	st=t.split('s', 1)
	try:
		time+=int(st[0])
        except:
		pass
	return str(time)
		

def skip(time):
	s = connect()
	s.sendall("SKIP\n")
        ok(s)
	s.sendall(time)
	sys.exit(0)

def seek(time):
	s = connect()
	s.sendall("SEEK\n")
        ok(s)
	s.sendall(time)
	sys.exit(0)

### Show usage

def helptext():
	print """kakrafoon [flags] [filenames...]
kakrafoon -r [-a] [user] [jobid...]

Plays audio files/urls on the sound system in T-salen.

Use the command 'telnet mixer' to pump up the volume.

Flags:
   -l, --long     show the queue with artists, song titles, etc.
   -q, --queue    show the queue with filenames/URLs
   -h, --help     show this text
   -r, --remove   remove a song from the queue
   -a, --all      delete all jobs (used with -r)
   -s, --skip <t> skip forward in song
   -S, --seek <t> seek to time in song
   -x, --example  show some example usage

Supported formats:
.mp3, .mp2, .ogg, .flac, .wav, .wma, .flv, .sid, .xm, .mod, .s3m, .mad, .it, youtube
"""
	sys.exit(0)

def examples():
	print """Play a song:
% kakrafoon ~/"Rick Astley - Never Gonna Give You Up.mp3"

Play the di.fm psychill stream:
% kakrafoon http://u14.di.fm:80/di_psychill

Play a song from youtube:
% kakrafoon http://www.youtube.com/watch?v=RcfXbHLQyQQ

Play a bunch of songs:
% kakrafoon ~/ogg/*ogg

Remove all songs queued by dr_root:
% kakrafoon -r dr_root

Remove all songs:
% kakrafoon -r -a

Remove the song with jobid 'sbUcq':
% kakrafoon -r sbUcq"""
	sys.exit(0)

#print 'ARGV      :', sys.argv[1:]

try:
	options, remainder = getopt.getopt(sys.argv[1:], 'hqlxr:s:S:', ['help', 
	'queue','list','example','remove=','skip=','seek='])
except:
	helptext()

#print 'OPTIONS   :', options

for opt, arg in options:
	if opt in ("-h", "--help"):
		helptext()
	elif opt in ("-q", "--queue"):
		queue()
	elif opt in ("-l", "--long"):
		queuehuman()
	elif opt in ("-r", "--remove"):
		remove(arg)
	elif opt in ("-x", "--example"):
		examples()
	elif opt in ("-s", "--skip"):
		skip(time_to_seconds(arg))
	elif opt in ("-S", "--seek"):
		seek(time_to_seconds(arg))

if len(sys.argv) < 2:
	helptext()

for file in sys.argv[1:]:
	sendfile(file)
