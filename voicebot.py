#!/usr/bin/python

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
import urllib2
from cStringIO import StringIO

# system imports
import sys, os.path, re
from time import gmtime, strftime

from irc.GenericIRCBot import GenericIRCBot, GenericIRCBotFactory, log
from TextToSpeech import TextToSpeech

FULLNAME = "VoiceBot v0.1"
BOTURL = "https://github.com/StevenVanAcker/VoiceBot"
DATAFILE = "/tmp/datafile"

allvoices = "mike crystal claire julia lauren mel ray rich rosa alberto".split(" ")

class VoiceBot(GenericIRCBot):
    def __init__(self): #{{{
        self.catchall = self.handle_catchall
	self.commandData = {
	    "!help": { 
	    	"fn": self.handle_HELP, 
		"argc": 0, 
		"tillEnd": False,
		"help": "this help text",
		"msgtypes": ["private"],
	    },
	    "!say": { 
	    	"fn": self.handle_SAY, 
		"argc": self.DontCheckARGC, 
		"tillEnd": True,
		"help": "say something",
		"msgtypes": ["private", "public", "directed"],
	    },
	    "!voices": { 
	    	"fn": self.handle_VOICES, 
		"argc": self.DontCheckARGC, 
		"tillEnd": True,
		"help": "list voices",
		"msgtypes": ["private", "public", "directed"],
	    },
	}
    #}}}
    def handle_VOICES(self, req): #{{{
	self.sendReply(req, "Voices: %s" % " ".join(allvoices))
	return
    #}}}
    def handle_SAY(self, req): #{{{
        txt = " ".join(req["words"][1:])
	voice = "rich"
    	if len(req["words"]) > 1 and req["words"][1].startswith("(") and req["words"][1].endswith(")"):
	    v = req["words"][1][1:-1]
	    if v in allvoices:
		txt = " ".join(req["words"][2:])
		voice = v
	    else:
	    	self.sendReply(req, "I don't know voice \"%s\", use !voices to get a list." % v)
		return
	     
        print "Asked to say as %s: %s" % (voice, txt)
	TextToSpeech(DATAFILE).add(txt, speaker="%s16" % voice)
#}}}
    def handle_catchall(self, req): #{{{
    	pass
#}}}

class VoiceBotFactory(GenericIRCBotFactory):
    def __init__(self, proto, channel, nick, password=None): #{{{
        GenericIRCBotFactory.__init__(self, proto, channel, nick, password)
# }}}


if __name__ == '__main__':
    # create factory protocol and application
    server = sys.argv[1] if len(sys.argv) > 1 else "irc.overthewire.org"
    port = 6667
    channels = ["#xxx"]
    password = None
    try:
	from config import *
    except:
    	pass
    f = VoiceBotFactory(VoiceBot, channels, "VoiceBot", password=password)

    # connect factory to this host and port
    reactor.connectSSL(server, port, f, ssl.ClientContextFactory())

    # run bot
    reactor.run()


