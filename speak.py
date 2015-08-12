#!/usr/bin/env python

def speak(txt=None, cmd="mplayer", defaultfile="/some/fail/file", speaker="rich16"): #{{{
    import sys, re, requests, tempfile, os, urllib
    fileToPlay = defaultfile
    deleteFile = False

    if not txt:
        txt = "Provide me with something to say, you idiot!"

    try:
	URL = 'http://www.wizzardspeech.com/att_demo.php' 
	HEADERS = { 
	    'Origin': ' http://www.wizzardspeech.com',
	    'Accept-Encoding': ' gzip, deflate',
	    'Accept-Language': ' en-US,en;q=0.8,nl;q=0.6,sv;q=0.4',
	    'Upgrade-Insecure-Requests': ' 1',
	    'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
	    'Content-Type': ' application/x-www-form-urlencoded',
	    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Cache-Control': ' max-age=0',
	    'Referer': ' http://www.wizzardspeech.com/att_demo.html',
	    'Connection': ' keep-alive'
	}

	DATADICT = {
	    "speaktext": txt,
	    "speaker": speaker
	}
	DATA = urllib.urlencode(DATADICT)

	r = requests.post(URL, headers=HEADERS, data=DATA)
	needles = re.findall(r'FlashVars="MyFile=([^"]+)"', r.text)

	if needles:
	    URL2 = 'http://www.wizzardspeech.com/php_tmp/' + needles[0]
	    HEADERS2 = {
		'Accept-Encoding': ' gzip, deflate, sdch',
		'Accept-Language': ' en-US,en;q=0.8,nl;q=0.6,sv;q=0.4',
		'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
		'Accept': ' */*',
		'Referer': ' http://www.wizzardspeech.com/att_demo.php',
		'X-Requested-With': ' ShockwaveFlash/18.0.0.209',
		'Connection': ' keep-alive'
	    }
	    r = requests.get(URL2, headers=HEADERS2)
	    fd, fn = tempfile.mkstemp()
	    fp = os.fdopen(fd, "w")
	    fp.write(r.content)
	    fp.close()

	    fileToPlay = fn
	    deleteFile = True
    except Exception,e:
	print "ERROR", e
    	pass
    os.system("%s %s" % (cmd, fileToPlay))
    if deleteFile:
	os.unlink(fileToPlay)
#}}}

