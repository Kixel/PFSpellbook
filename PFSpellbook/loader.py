

import requests as req
import os
import tools.persistent_naming as pn
from tools.spell import Spell
from abc import ABC, abstractmethod
from typing import Any
import configparser
import time
import random
import urllib.parse
from xml.dom import minidom
import qrcode
import qrcode.image.svg
import pprint as pp


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
            cl_max = 1
            cl_interval = 5
            cl_random = 3
            unusuals = []
            for cline in lines:
                if cl_i >= cl_max:
                    break
                cl_i = cl_i + 1
                clineparts = cline.split(pn.csvseparator)
                sname = clineparts[0]
                fname = pn.spell2filename(sname)
                dldata = ""
                flink = clineparts[1].replace("\n", "")
                flink_clean = urllib.parse.quote(flink, safe=":/?&=")
                print("[?] #"+str(cl_i)+" Spellname: "+sname)
                if not os.path.exists(os.path.join(self._cachebase, fname)):
                    os.makedirs(os.path.join(self._cachebase, fname))
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
                        
                #create qr code if not existing
                if not os.path.exists(os.path.join(self._cachebase, fname, "qr.svg")):
                    with open(os.path.join(self._cachebase, fname, "qr.svg"), 'wb') as qr:
                        qrimg = qrcode.make(flink_clean, image_factory=qrcode.image.svg.SvgImage)
                        #qrf = qrcode.QRCode(error_correction = qrcode.constants.ERROR_CORRECT_H)
                        #qrf.add_data(qr)
                        #aa = qrf.make(fit=True)
                        qrimg.save(qr)
                #code to parse that file TODO
                dl_bottom = dldata.split('<span id="ctl00_MainContent_DataListTypes_ctl00_LabelName">', 1)[1]
                dl_data = "<span>" + dl_bottom.split("\n", 1)[0]
                print(dl_data)
                ##clear images
                dl_data = dl_data.replace("<img", "??img")
                spelldoc = minidom.parseString(dl_data)
                foundspell = False
                newspell = Spell()
                currentfeature = ""
                for node in spelldoc.childNodes[0].childNodes:
                    if node.nodeName == "h1":
                        childdata = node.childNodes[0].data
                        lastthing = childdata.split('">')[-1].lstrip(" ").rstrip(" ")
                        if not foundspell:
                        #seek to current spell in case of multiple spells
                            if sname == lastthing:
                                foundspell = True       
                        else:
                            if not (sname == lastthing):
                                foundspell = False
                    if foundspell:
                        if node.nodeName == "#text":
                            if node.data == " " or node.data == ", " or node.data == " (" or node.data == ") [" or node.data == "]; ":
                                continue
                        if currentfeature == "description":
                            newspell.description = newspell.description + node.toxml()
                            continue
                        elif currentfeature == "source":
                            if node.nodeName == "a":
                                if node.firstChild.nodeName == "i":
                                    try:
                                        newspell.source.append(node.firstChild.firstChild.data)
                                        newspell.source.append(node.firstChild.firstChild.data.split("pg.")[0])
                                    except:
                                        unusuals.append(node.toxml())
                            else:
                                unusuals.append(node.toxml())
                        
                        if node.nodeName == "h1":
                            newspell.name = sname
                            newspell.url = flink_clean
                            if "ThreeFiveSymbol.gif" in node.childNodes[0].data:
                                newspell.threefive = True
                            if "PathfinderSocietySymbol.gif" in node.childNodes[0].data:
                                newspell.pfslegal = True
                            if "PathfinderSocietySymbolN.gif" in node.childNodes[0].data:
                                newspell.pfsrestricted = True
                        if node.nodeName == "b":
                            bcontent = node.firstChild.data
                            if bcontent == "Source":
                                currentfeature = "source"
                            elif bcontent == "School":
                                currentfeature = "school"
                            elif bcontent == "Level":
                                currentfeature = "level"
                            elif bcontent == "Casting Time":
                                currentfeature = "casttime"
                            elif bcontent == "Components":
                                currentfeature = "components"
                            elif bcontent == "Range":
                                currentfeature = "range"
                            elif bcontent == "Target":
                                currentfeature = "target"
                            elif bcontent == "Duration":
                                currentfeature = "duration"
                            elif bcontent == "Saving Throw":
                                currentfeature = "save"
                            elif bcontent == "Spell Resistance":
                                currentfeature = "sr"
                            elif bcontent == "Description":
                                currentfeature = "description"
                        
                        
                        
                        
                        
                        
                pp.pprint(newspell.__dict__)
                        
                        
                
            
            
            
        
class FIVEFOOTSTEP(AnyLoader):
    
    def __init__(self, sourcefile: str):
        super().__init__(sourcefile)