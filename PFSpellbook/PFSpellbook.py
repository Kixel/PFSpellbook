

import argparse
import jinja2




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

if __name__ == "__main__":
    print("="*100+"\n                  Pathfinder 1E Spellbook Generator\n"+bookart+"\n"+"="*100)
    ap = argparse.ArgumentParser(prog="Pathfinder Spellbook Generator")
    ap.add_argument("-r", "--rip", action="store", choices=choicesforR, help="Rips data from the specified source before doing anything else. If not specified, will use available data, or exit if nothing is found.")
    ap.add_argument("-s", "--storedata", action="store_true", help="Stores ripped data for later use.")
    ap.add_argument("-c", "--combinerip", action="store_true", help="Will append and replace old data, not completely remove old data and rewrite it")
    
    t = ap.parse_args()


