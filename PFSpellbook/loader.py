

import requests as req
import os
import tools.persistent_naming as pn
from abc import ABC, abstractmethod
from typing import Any
import configparser
import time
import random
import urllib.parse


class AnyLoader(ABC):
    delaybetweenrequests = 1000
    variationbetweenrequests = 500
    overviewfilename = "listall.html"
    linkcache = "linkcache.csv"
    
    def __init__(self, sourcefile: str):
        self._src = sourcefile
        self._config = configparser.ConfigParser()
        self._config.read(self._src)        
        self._cachebase = ""
    
    @staticmethod
    def getLoader(sourcefile: str):
        if "5footstep.ini" in sourcefile:
            return FIVEFOOTSTEP(sourcefile)
        elif "aon.ini" in sourcefile:
            return AON(sourcefile)
        elif "d20pfsrd.ini" in sourcefile:
            return D20PFSRD(sourcefile)
        else:
            raise TypeError("Invalid ini file: "+sourcefile+" is not recognised!")
        pass    
    
    @abstractmethod
    def ripFromSource(self, cachefolder : str) -> bool:
        pass
        
        
class D20PFSRD(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)
        
        
class AON(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)
        self._aonspellpagebase = "https://www.aonprd.com/"
        
        
    def ripFromSource(self, cachefolder : str) -> bool:
        self._cachebase = os.path.join(cachefolder, "aon")
        if not os.path.exists(self._cachebase):
            print("[?] Cache folder does not exist. Creating folders.")
            os.makedirs(self._cachebase)
        pagedata = ""
        if not os.path.exists(os.path.join(self._cachebase, self.overviewfilename)):
            print("[?] Overview list not in folder, downloading from source")
            print("[?] Source: " + self._config.get("urls", "ALL"))
            pagereq = req.get(self._config.get("urls", "ALL"))
            pagedata = pagereq.text
            with open(os.path.join(self._cachebase, self.overviewfilename), 'w') as pagewriter:
                pagewriter.write(pagedata)
        else:
            print("[?] Using cached version of "+self.overviewfilename)
            with open(os.path.join(self._cachebase, self.overviewfilename), 'r') as pagereader:
                pagedata = pagereader.read()
        lowerhalf = pagedata.split('<table id="ctl00_MainContent_DataListTypes" cellspacing="0" border="0" style="border-collapse:collapse;">', 1)[1]
        middlehalf = lowerhalf.split("</table>", 1)[0]
        spelllines = middlehalf.split("</tr>")
        print("[?] Found total of spells: "+str(len(spelllines)))
        if not os.path.exists(os.path.join(self._cachebase, self.linkcache)):
            print("[?] No link cache found. Parsing " + self.overviewfilename)
            with open(os.path.join(self._cachebase, self.linkcache), 'w') as quickcsv:
                for sline in spelllines:
                    if not "SpellDisplay" in sline:
                        print("[?] Skipping unknown line: " + sline)
                        continue
                    nl = ""
                    lowerpart = sline.split('<a href="', 1)[1]
                    urlgrabber = lowerpart.split('">', 1)
                    nurl = self._aonspellpagebase + urlgrabber[0]
                    namegrabber = urlgrabber[1].split('</a>', 1)[0]
                    name = namegrabber.split('">')[-1]
                    namecleaned = name.split("</b><sup>")[0]
                    nl = nl + namecleaned.lstrip(" ") + pn.csvseparator + nurl + "\n"
                    #print(name, nurl)
                    quickcsv.write(nl)
        with open(os.path.join(self._cachebase, self.linkcache), 'r') as linkcachereader:
            lines = linkcachereader.readlines()
            cl_i = 0
            cl_max = 5000
            cl_interval = 5
            cl_random = 3
            for cline in lines:
                if cl_i >= cl_max:
                    break
                cl_i = cl_i + 1
                clineparts = cline.split(pn.csvseparator)
                sname = clineparts[0]
                fname = pn.spell2filename(sname)
                dldata = ""
                print("[?] #"+str(cl_i)+" Spellname: "+sname)
                if not os.path.exists(os.path.join(self._cachebase, fname)):
                    os.makedirs(os.path.join(self._cachebase, fname))
                    flink = clineparts[1].replace("\n", "")
                    flink_clean = urllib.parse.quote(flink, safe=":/?&=")
                    print("[?] Downloading from "+flink_clean)
                    dldata = req.get(flink_clean).text
                    with open(os.path.join(self._cachebase, fname, "rawdata.html"), 'w') as rawwriter:
                        rawwriter.write(dldata)
                    randomoffset = random.random()*(cl_random*2)-cl_random
                    totalsleep = 5+randomoffset
                    print("[?] Sleeping for "+str(totalsleep)+" seconds")
                    time.sleep((cl_interval+totalsleep))
                else:
                    with open(os.path.join(self._cachebase, fname, "rawdata.html"), 'r') as rawreader:
                        dldata = rawreader.read()
                        print("[?] Found data in cache folder")
                #code to parse that file TODO
                    
                
                
            
            
            
        
class FIVEFOOTSTEP(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)