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
	}
    #}}}
    def handle_SAY(self, req): #{{{
        txt = " ".join(req["words"][1:])
	voice = "rich"
    	if len(req["words"]) > 1 and req["words"][1].startswith("(") and req["words"][1].endswith(")"):
	    txt = " ".join(req["words"][2:])
	    voice = req["words"][1][1:-1]
	     
        print "Asked to say: %s" % txt
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


