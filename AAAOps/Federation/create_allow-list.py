import subprocess
import sys

BASE = "/root/fgomezco_test/tmp"

redirectors = [ "cms-xrd-global01.cern.ch:1094", 
                "cms-xrd-global02.cern.ch:1094", 
                "cms-xrd-transit.cern.ch:1094"]

for redirector in redirectors[:]:
    out_name = 'tmp_out_'+ str(redirector)
    err_name = 'tmp_err_'+ str(redirector)
    with open(out_name,'w+') as fout:
        with open(err_name,'w+') as ferr:
            out=subprocess.call(["ls",'-lha'],stdout=fout,stderr=ferr) # Python 3.5+, use subprocess.run() 
            # reset file to read from it
            fout.seek(0)
            ferr.seek(0) 
            # save output (if any) in variable
            output=fout.read()
            errors = ferr.read()

