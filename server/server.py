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
import _winreg
import hashlib
from subprocess import Popen, PIPE, CREATE_NEW_PROCESS_GROUP

from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from vendor import appdirs
from vendor import tmdb3 as themoviedb


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)


def _getDatabaseLocation():
    """
    """
    parent = appdirs.user_data_dir("ka-boom", "nikola", roaming=True)

    if not os.path.exists(parent):
        os.makedirs(parent)

    location = parent

    if platform.system() == "Windows":
        location = location.replace("\\", r"\\\\")
        location = location + r"\\\\data"
    else:
        sys.exit(1)

    return location


def _getChromeExePath():
    """
    """
    registry = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    try:
        key = _winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
    except WindowsError:
        return None
    else:
        exePath = _winreg.QueryValueEx(key, "Path")[0]
        key.Close()
        return exePath


def _getChromeApplicationId(pathname):
    """
    """
    if (len(pathname) > 1 and pathname[0].islower() and pathname[1] == ":"):
        pathname = pathname[0].upper() + pathname[1:]

    if platform.system() == "Windows":
        pathname = pathname.encode("utf-16le")

    offset = ord("a")
    applicationId = "".join([chr(int(digit, 16) + offset) for digit in hashlib.sha256(pathname).hexdigest()[:32]])

    return applicationId


def _extractRawMetadataFromPathname(dirname):
    """
    """
    releaseYear = 2013
    editVersion = "Theatrical Cut"
    extractedTitle = None

    searchReleaseYear = re.compile(r"(?<!^)((19|20)\d{2})[a-zA-Z0-9\.\-\) '\[\]]*$").search(dirname)
    if searchReleaseYear is not None:
        releaseYear = int(searchReleaseYear.groups()[0])
        rawTitle = re.search("^(.*)(?=%s)" % releaseYear, dirname).groups()[0]
    else:
        rawTitle = dirname

    intermediateTitle = rawTitle

    # Remove special characters.
    intermediateTitle = re.compile(r"[\(\[,\-]").sub(" ", intermediateTitle)

    # Convert dots to spaces (except when followed by a zero).
    intermediateTitle = re.compile(r"\.(?!0)").sub(" ", intermediateTitle)

    # Remove superfluous multi-angle indicators.
    intermediateTitle = re.compile(r"\d[\- ]*in[\- ]*\d").sub("", intermediateTitle).strip()

    # Remove superfluous edition indicator.
    intermediateTitle = re.compile(r"(?<= )special edition(?= |$)", re.I).sub(" ", intermediateTitle).strip()

    # Remove superfluous cut indicator.
    intermediateTitle = re.compile("(?<= )hybrid(?= |$)", re.I).sub(" ", intermediateTitle).strip()

    # Remove superfluous source indicator.
    intermediateTitle = re.compile("(?<= )(2|3)d source(?= |$)", re.I).sub(" ", intermediateTitle).strip()

    # Remove superfluous frame indicator.
    intermediateTitle = re.compile("(?<= )open matte(?= |$)", re.I).sub(" ", intermediateTitle).strip()

    # Collapse multiple spaces.
    intermediateTitle = re.compile("  +").sub(" ", intermediateTitle)

    # Extract cut indicator.
    searchCutIndicator = re.compile(r"((extended|final|theatrical|international|director[ ']s?) cut)$", re.I).search(intermediateTitle)
    if searchCutIndicator is not None:
        editVersion = searchCutIndicator.groups()[0]
        intermediateTitle = re.compile(r"((extended|final|theatrical|international|director[ ']s?) cut)$", re.I).sub("", intermediateTitle)
    # else:
    #     cutIndicator = "Theatrical Cut"

    # Remove leading Roman numerals.
    intermediateTitle = re.compile(r"^X?(IX|IV|V?I{0,3}) ").sub("", intermediateTitle)

    # Remove surrounding whitespace.
    intermediateTitle = intermediateTitle.strip()

    return {
        "extractedTitle": intermediateTitle,
        "releaseYear":    releaseYear,
        "editVersion":    editVersion,
    }


def _visitDirectory(top):
    """
    """
    themoviedb.set_key("ef89c0a371440a7226e1be2ddfe84318")
    themoviedb.set_cache("null")
    themoviedb.set_locale("de", "de")

    for root, dirs, files in os.walk(top):
        dirname = re.compile(r"[a-z]\:\/\/", re.I).sub("", root)

        # Skip directories which contain no movie files.
        if not any([True for name in files if name.endswith((".mkv", ".MKV"))]) or re.compile(r"\\!?sample$", re.I).search(dirname) is not None: continue

        # Ignore parent directory for the time being.
        if dirname.find("\\") != -1:
            dirname = re.compile(r"(?<=\\).*$").search(dirname).group()

        # Remove leading underscore.
        dirname = re.compile(r"^_ +").sub("", dirname).strip()

        rawMetadata = _extractRawMetadataFromPathname(dirname)
        releaseYear = rawMetadata["releaseYear"]

        # 30 requests every 10 seconds per IP

        results = themoviedb.searchMovie(query=rawMetadata["extractedTitle"].encode("utf-8"), year=releaseYear)

        if not len(results):
            results = themoviedb.searchMovie(query=rawMetadata["extractedTitle"].encode("utf-8"))
    
        if len(results):
            print "%s -> %s" % (rawMetadata["extractedTitle"], repr(results[0].title))
        else:
            print "??? %s" % rawMetadata["extractedTitle"]
        time.sleep(0.5)

        # print "%s (%s, %d)" % (rawMetadata["extractedTitle"], rawMetadata["editVersion"], rawMetadata["releaseYear"])


if __name__ == "__main__":
    # Pass Unicode string as root so we get Unicode directory names later on.
    _visitDirectory(u"M://")
    
    sys.exit()

    dsn = "sqlite:///" + _getDatabaseLocation()
 
    engine = create_engine(dsn, echo=False, module=sqlite)
    # engine.execute("select 1").scalar()

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    
    session = Session()
    ed_user = User('ed', 'Ed Jones', 'edspassword')
    session.add(ed_user)
    session.commit()

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

    p = Popen('"C:\Users\Niko\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --profile-directory=Default --app-id=ainpgneglbdpnfikehealafocjcfaoei', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    # p = Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --profile-directory=Default --load-and-launch-app=C:\Users\Niko\Documents\GitHub\ka-BOOM\client', stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    assert not p.poll()
