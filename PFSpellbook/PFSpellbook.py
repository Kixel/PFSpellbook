

import argparse
import jinja2
import os
import glob

indir = "./in"
outdir = "./out"
cachedir = "./cache"

defaulttemplate = "defaultall"

choicesforR = ["d20pfsrd", "aon", "5footstep"]
bookart = """
                 __...--~~~~~-._   _.-~~~~~--...__
               //               `V'               \\ 
              //                 |                 \\ 
             //__...--~~~~~~-._  |  _.-~~~~~~--...__\\ 
            //__.....----~~~~._\ | /_.~~~~----.....__\\
           ====================\\|//====================
                               `---`
"""



def getAvailableTemplates() -> list:
    #print(os.listdir("."))
    avtemp = [fn for fn in os.listdir("./templates") if fn.endswith(".html")]
    #print(avtemp)
    avtemp.append("custom")
    return avtemp
    
    
    

def parseArgs() -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="Pathfinder Spellbook Generator")
    ap.add_argument("-i", "--interactive", action="store_true", help="Starts PFSpells in interactive mode")
    
    ap.add_argument("-r", "--rip", action="store", choices=choicesforR, help="Rips data from the specified source before doing anything else. If not specified, will use available data, or exit if nothing is found.")
    ap.add_argument("-s", "--storedata", action="store_true", help="Stores ripped data for later use.")
    ap.add_argument("-m", "--mergerip", action="store", nargs="?", help="Will append and replace old data, not completely remove old data and rewrite it")
    ap.add_argument("-c", "--cachelocation", action="store", help="Change the location of the data cache")
    
    ap.add_argument("-f", "--filter", action="store", help="a csv file to filter the spellbook output")
    ap.add_argument("-t", "--template", action="store", choices=getAvailableTemplates(), help="the name of the template", default=defaulttemplate)
    ap.add_argument("--custom-template", action="store", help="Add the path to another compatible html file for a template here", default="")
    
    ap.add_argument("-b", "--build", action="store_true", help="Parse the cached data to an output file")
    ap.add_argument("-o", "--output", action="store", help="Set the output file name and location", default="./spellbook.pdf")
    t = ap.parse_args()
    return t
    

def updateEnv():
    if os.environ.get("ISDOCKER", False):
        print("[?] This is a docker environment!")
        print("[?] Please ensure you have mounted folders to /in, /out and /cache")
    else:
        print("[?] Running in CLI mode")
        global indir, outdir
        indir = ""
        outdir = ""
        
def phaseRip(args):
    pass

def phaseBuild(args):
    pass

def runPFSpells():
    print("="*100+"\n                  Pathfinder 1E Spellbook Generator\n"+bookart+"\n"+"="*100)
    updateEnv()
    arg = parseArgs()    
    if arg.interactive:
        #TODO: add interactive mode :-/
        print("Interactive mode is not available yet (╯°□°）╯︵ ┻━┻")    
        return False
    if arg.template == "custom" and arg.custom_template == "":
        print("If template (-t) is set to custom, a valid --custom-template must be provided!")
        return False
    phaseRip(arg)
    phaseBuild(arg)    


if __name__ == "__main__":
    runPFSpells()    

