# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2013 Nikola Klaric"

import sys
import os
import re
import time
import platform

from subprocess import Popen, PIPE, CREATE_NEW_PROCESS_GROUP

from sqlalchemy.orm import sessionmaker
from utils.collector import *
from utils.db import *
from utils.win32 import *


from vendor import tmdb3 as themoviedb


if __name__ == "__main__":
    if platform.system() != "Windows":
        sys.exit()

    streamManager = StreamManager()

    sys.exit()

    for (path, container) in getMoviePathnames("M://"):
        basedata = getBasedataFromPathname(container)
        print basedata["extractedTitle"]

    # print "%s (%s, %d)" % (rawMetadata["extractedTitle"], rawMetadata["editVersion"], rawMetadata["releaseYear"])

    sys.exit()


    themoviedb.set_key("ef89c0a371440a7226e1be2ddfe84318")
    themoviedb.set_cache("null")
    themoviedb.set_locale("de", "de")

    # 30 requests every 10 seconds per IP

    results = themoviedb.searchMovie(query=rawMetadata["extractedTitle"].encode("utf-8"), year=releaseYear)

    if not len(results):
        results = themoviedb.searchMovie(query=rawMetadata["extractedTitle"].encode("utf-8"))

    if len(results):
        print "%s -> %s" % (rawMetadata["extractedTitle"], repr(results[0].backdrop.geturl()))
    else:
        print "??? %s" % rawMetadata["extractedTitle"]
    time.sleep(0.5)




    
    # session = Session()
    # ed_user = User('ed', 'Ed Jones', 'edspassword')
    # session.add(ed_user)
    # session.commit()

    # session.query(User).filter("id<:value and name=:name").params(value=224, name='ed').order_by(User.id).one()

    print _getChromeApplicationId(r"C:\Users\Niko\Documents\GitHub\ka-BOOM\client")

    print _getChromeExePath()
    

    sys.exit()

    kwargs = {}
    DETACHED_PROCESS = 0x00000008          
    kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)  

    # chrome.exe –enable-easy-off-store-extension-install
    # https://code.google.com/p/chromium/issues/detail?id=138995
    # http://www.chromium.org/administrators/policy-list-3#ExtensionInstallSources

    # prompt to install extension: chrome.exe --new-window https://github.io/ka-boom


    # check for installation: C:\Users\Niko\AppData\Local\Google\Chrome SxS\User Data\Default\Web Applications\_crx_ainpgneglbdpnfikehealafocjcfaoei

    # http://peter.sh/experiments/chromium-command-line-switches/

    # --app-id -> Specifies that the extension-app with the specified id should be launched according to its configuration.
    # ??? --force-app-mode -> Forces application mode. This hides certain system UI elements and forces the app to be installed if it hasn't been already.
    # ??? --enable-ephemeral-apps -> Enables experimentation with ephemeral apps, which are launched without installing in Chrome.
    #     --load-and-launch-app -> Loads an app from the specified directory and launches it.


    """
    --host-rules
    Comma-separated list of rules that control how hostnames are mapped. For example: "MAP * 127.0.0.1" --> Forces all hostnames to be mapped to 127.0.0.1 "MAP *.google.com proxy" --> Forces all google.com subdomains to be resolved to "proxy". "MAP test.com [::1]:77 --> Forces "test.com" to resolve to IPv6 loopback. Will also force the port of the resulting socket address to be 77. "MAP * baz, EXCLUDE www.google.com" --> Remaps everything to "baz", except for "www.google.com". These mappings apply to the endpoint host in a net::URLRequest (the TCP connect and host resolver in a direct connection, and the CONNECT in an http proxy connection, and the endpoint host in a SOCKS proxy connection).
    """

    # ALL WRONG??
    # --load-and-launch-app -> no installation, but runs

    # FIRST RUN:
    # --no-startup-window ?????
    # p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --no-startup-window --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    # p = Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --no-startup-window --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)

    # AFTER INSTALLATION:
    # p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --app-id=ainpgneglbdpnfikehealafocjcfaoei', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)

    # p = Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --enable-ephemeral-apps --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    assert not p.poll()

    """

        p.pid == The process ID of the child process


        import ctypes

        def kill(pid):
            
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(1, 0, pid)
            return (0 != kernel32.TerminateProcess(handle, 0))


    """




    """

# Helper function that sends a message to the webapp.
21  def send_message(message):
22     # Write message size.
23    sys.stdout.write(struct.pack('I', len(message)))
24    # Write the message itself.
25    sys.stdout.write(message)
26    sys.stdout.flush()

    """
