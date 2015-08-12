#!/usr/bin/env python

from lockfile import FileLock
from speak import speak
import sys, time

class TextToSpeech(object):

    def __init__(self, fn, cmd="mplayer", speaker="rich16"): #{{{
	self.command = cmd
	self.defaultspeaker = speaker
        self.filename = fn
	self.lockfile = fn + ".lock"
#}}}
    def add(self, line, speaker=None): #{{{
	if speaker == None:
	    speaker=self.defaultspeaker
	with FileLock(self.lockfile, threaded=False):
	    with open(self.filename, "a") as fp:
		fp.write("%s %s\n" % (speaker, line))
#}}}
    def consumeOne(self): #{{{
	toplay = None
	voice = None
	with FileLock(self.lockfile, threaded=False):
	    try:
		lines = [x.strip() for x in open(self.filename, "r").readlines()]
		if len(lines) > 0:
		    a, b = lines[0].split(" ", 1)
		    rest = lines[1:]
		    with open(self.filename, "w") as fp:
			fp.write("\n".join(rest))
		    voice, toplay = a,b
	    except IOError:
		pass
	if toplay:
	    speak(toplay, cmd=self.command, speaker=voice)
#}}}
    def consume(self): #{{{
        while True:
	    self.consumeOne()
	    time.sleep(0.2)
#}}}

if __name__ == "__main__":
    t = TextToSpeech(sys.argv[1])
    t.consume()
