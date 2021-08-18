import subprocess
import sys
from pprint import pprint

TMPBASE = "/root/fgomezco_test/tmp/"
ENV="dev"

def get_raw_global_redirectors():
    redirectors = [ "cms-xrd-global01.cern.ch:1094", 
                    "cms-xrd-global02.cern.ch:1094", 
                    "cms-xrd-transit.cern.ch:1094"]

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
        names_only = []

        for r in output.splitlines():
            aux = r.split()
            if len(aux) == 2:
                aux.insert(0, "no-level")
            redir_prep.append(aux)

            name = aux[-1].split(":")[0] #Remove port
            names_only.append(name)

        names_only = list(set(names_only))

        redir_raw.append({"name":redirector, 
                          "location":"CERN" ,
                          "raw_out":output.splitlines(),
                          "error": errors.splitlines(),
                          "redir_prep": redir_prep,
                          "names_only": names_only})
    return redir_raw

def get_raw_eu_redirectors(global_name, list_names):
    
    european = ["xrootd.ba.infn.it",
                "xrootd-redic.pi.infn.it", 
                "llrxrd-redir.in2p3.fr"]
    
    redirectors=[]
    for name in list_names:
        if name in european:
            redirectors.append(name + ":1094")

    redir_raw = []
    for redirector in redirectors[:]:
        out_name = TMPBASE + 'tmp_out_european_'+ str(redirector)
        err_name = TMPBASE + 'tmp_err_european_'+ str(redirector)

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
        names_only = []

        for r in output.splitlines():
            aux = r.split()
            if len(aux) == 2:
                aux.insert(0, "no-level")
            redir_prep.append(aux)

            nameWport = aux[-1].split(":")
            if len(nameWport) == 2:
                name = nameWport[0]
                names_only.append(name) 
            else: # Cases like: [2001:67c:1bec:f069::169]:1095
                name = aux[-1].split("]:")[0]
                names_only.append(name + "]")

        names_only = list(set(names_only))

        redir_raw.append({"global_parent":global_name,
                         "name":redirector, 
                         "location":"Europe" ,
                         "raw_out":output.splitlines(),
                         "error": errors.splitlines(),
                         "redir_prep": redir_prep,
                         "names_only": names_only})
    return redir_raw



def get_raw_us_redirectors(global_name, list_names):
    
    american = ["cmsxrootd2.fnal.gov",
                "xrootd.unl.edu"]
    
    redirectors=[]
    for name in list_names:
        if name in american:
            redirectors.append(name + ":1094")

    redir_raw = []
    for redirector in redirectors[:]:
        out_name = TMPBASE + 'tmp_out_american_'+ str(redirector)
        err_name = TMPBASE + 'tmp_err_american_'+ str(redirector)

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
        names_only = []

        for r in output.splitlines():
            aux = r.split()
            if len(aux) == 2:
                aux.insert(0, "no-level")
            redir_prep.append(aux)

            nameWport = aux[-1].split(":")
            if len(nameWport) == 2:
                name = nameWport[0]
                names_only.append(name) 
            else: # Cases like: [2001:67c:1bec:f069::169]:1095
                name = aux[-1].split("]:")[0]
                names_only.append(name + "]")

        names_only = list(set(names_only))

        redir_raw.append({"global_parent":global_name,
                         "name":redirector,
                         "location":"America" ,
                         "raw_out":output.splitlines(),
                         "error": errors.splitlines(),
                         "redir_prep": redir_prep,
                         "names_only": names_only})
    return redir_raw







if __name__ == '__main__':
    print(" I AM MAIN")

else:
    print('I AM NOT MAIN')

    print(">>  Get global redirectors")
    global_raw = get_raw_global_redirectors()
    print(">>  Get global redirectors: DONE")

    eu_raw = []
    us_raw = []

    for red in global_raw:
        #pprint(red["redir_prep"])
        print(red['name'])
        print(red['names_only'])

        print(">>>>  Get EU redirector")
        eu_redir = get_raw_eu_redirectors(red['name'], red['names_only'])
        eu_raw.extend(eu_redir)
        print(">>>>  Get EU redirector: DONE")

        print(">>>>  Get US redirector")
        eu_redir = get_raw_us_redirectors(red['name'], red['names_only'])
        eu_raw.extend(eu_redir)
        print(">>>>  Get US redirector: DONE")

    for red in us_raw:
        print(red['name'])
        pprint(red["redir_prep"])
        print()

    