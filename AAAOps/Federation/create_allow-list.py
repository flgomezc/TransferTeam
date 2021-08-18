import subprocess
import sys
from pprint import pprint

TMPBASE = "/root/fgomezco_test/tmp/"
ENV="dev"

redirectors = [ "cms-xrd-global01.cern.ch:1094", 
                "cms-xrd-global02.cern.ch:1094", 
                "cms-xrd-transit.cern.ch:1094"]

def get_raw_global_redirectors():
    redir_raw = []

    for redirector in redirectors[:]:
        out_name = TMPBASE + 'tmp_out_'+ str(redirector)
        err_name = TMPBASE + 'tmp_err_'+ str(redirector)

        if ENV == "prod":
            with open(out_name,'w+') as fout:
                with open(err_name,'w+') as ferr:
                    print(">>> xrdmapc --list all " + redirector)
                    # run xrdmapc
                    out=subprocess.call(["xrdmapc", "--list", "all", 
                            redirector], stdout=fout,stderr=ferr) 
                    # TODO Python 3.5+, use subprocess.run() 
                
                    # If not in prod, just read existing files.             
                    # Go to the head of the file, and save in variable
                    fout.seek(0)
                    ferr.seek(0)              
                    output=fout.read()
                    errors = ferr.read()
        else:
            with open(out_name,'r') as fout:
                with open(err_name,'r') as ferr:
                    output=fout.read()
                    errors = ferr.read()
            
        redir_prep = []
        for r in output.splitlines():
            aux = r.split()
            redir_prep.append(aux)


        redir_raw.append({"name":redirector, 
                          "raw_out":output.splitlines(),
                          "error": errors.splitlines(),
                          "redir_prep": redir_prep})
    return redir_raw

def get_raw_eu_redirectors():
    return 0


if __name__ == '__main__':

    print(">>  Get global redirectors")
    global_raw = get_raw_global_redirectors()

    for red in global_raw:
        pprint(red["redir_prep"])
    