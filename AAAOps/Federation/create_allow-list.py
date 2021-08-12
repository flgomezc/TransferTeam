import subprocess
import sys
from pprint import pprint

TMPBASE = "/root/fgomezco_test/tmp/"

redirectors = [ "cms-xrd-global01.cern.ch:1094", 
                "cms-xrd-global02.cern.ch:1094", 
                "cms-xrd-transit.cern.ch:1094"]

def get_raw_global_redirectors():
    redir_raw = []

    for redirector in redirectors[:]:
        out_name = TMPBASE + 'tmp_out_'+ str(redirector)
        err_name = TMPBASE + 'tmp_err_'+ str(redirector)

        with open(out_name,'w+') as fout:
            with open(err_name,'w+') as ferr:
                print(">>> xrdmapc --list all " + redirector)
                out=subprocess.call(["xrdmapc", "--list", "all", redirector],
                                    stdout=fout,stderr=ferr) 
                # TODO Python 3.5+, use subprocess.run() 
                
                # reset file to read from it
                fout.seek(0)
                ferr.seek(0) 
                # save output (if any) in variable
                output=fout.read()
                errors = ferr.read()
    
                redir_raw.append({"name":redirector, 
                                  "output":output.splitlines(),
                                  "error": errors.splitlines()})
    return redir_raw

def get_raw_eu_redirectors():
    return 0


if __name__ == '__main__':
    global_raw = get_raw_global_redirectors()

    pprint(global_raw)
    