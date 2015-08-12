#!/usr/bin/python

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import urllib2
from cStringIO import StringIO

# system imports
import sys, os.path, re
from time import gmtime, strftime

from irc.GenericIRCBot import GenericIRCBot, GenericIRCBotFactory, log
from speak import speak

FULLNAME = "VoiceBot v0.0"
BOTURL = "nowhere"

try:
    import Image
    import aalib
    use_aalib = True
except ImportError:
    use_aalib = False
    print "aalib not found on this system..."

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
        print "Asked to say: %s" % txt
	speak(txt)
#}}}
    def handle_catchall(self, req): #{{{
    	pass
#}}}

class VoiceBotFactory(GenericIRCBotFactory):
    def __init__(self, proto, channel, nick): #{{{
        GenericIRCBotFactory.__init__(self, proto, channel, nick)
# }}}


if __name__ == '__main__':
    # create factory protocol and application
    f = VoiceBotFactory(VoiceBot, ["#xxx"], "VoiceBot")

    # connect factory to this host and port
    reactor.connectTCP(sys.argv[1] if len(sys.argv) > 1 else "irc.overthewire.org", 6667, f)

    # run bot
    reactor.run()


