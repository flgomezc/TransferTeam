import subprocess
import sys
from pprint import pprint

TMPBASE = "/root/fgomezco_test/tmp/"
FEDINFO = "/root/fgomezco_test/fgomezco_dev/TransferTeam/AAAOps/Federation"
#TMPBASE = "/root/tmp/"
#FEDINFO=/opt/TransferTeam/AAAOps/Federation/
ENV="dev"

def xrdmapc_list_all_(redirector, global_parent, location):

    out_name = TMPBASE + "tmp_" + location + "_out_" + str(redirector)
    err_name = TMPBASE + "tmp_" + location + "_err_" + str(redirector)

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
    nameport = []

    for r in output.splitlines():
        aux = r.split()
        if len(aux) == 2:
            aux.insert(0, "no-level")
        redir_prep.append(aux)
        nameport.append(aux[2])

        nameWport = aux[-1].split(":")
        if len(nameWport) == 2:
            name = nameWport[0]
            names_only.append(name) 
        else: # Cases like: [2001:67c:1bec:f069::169]:1095
            name = aux[-1].split("]:")[0]
            names_only.append(name + "]")

            # TODO handle cases like:
            # Unable to get osg-se.sprace.org.br:1094 subscribers; [ERROR] Operation expired

    names_only = list(set(names_only))

    redir_info = {"global_parent":global_parent,
                        "name":redirector,
                        "location":location,
                        "nameport":nameport,
                        "raw_out":output.splitlines(),
                        "error": errors.splitlines(),
                        "redir_prep": redir_prep,
                        "names_only": names_only}
    
    return redir_info

def get_raw_global_redirectors():
    redirectors = [ "cms-xrd-global01.cern.ch:1094", 
                    "cms-xrd-global02.cern.ch:1094", 
                    "cms-xrd-transit.cern.ch:1094"]
    global_parent = "None"
    location = "CERN"

    redir_raw = []
    for redirector in redirectors[:]:
        redir_info = xrdmapc_list_all_(redirector, global_parent, location)
        redir_raw.append(redir_info)
    return redir_raw

def get_raw_eu_redirectors(global_parent, list_names):
    european = ["xrootd.ba.infn.it",
                "xrootd-redic.pi.infn.it", 
                "llrxrd-redir.in2p3.fr"]
    location = "Europe"

    redirectors=[]
    for name in list_names:
        if name in european:
            redirectors.append(name + ":1094")

    redir_raw = []
    for redirector in redirectors[:]:
        redir_info = xrdmapc_list_all_(redirector, global_parent, location)
        redir_raw.append(redir_info)
    return redir_raw

def get_raw_us_redirectors(global_parent, list_names):
    american = ["cmsxrootd2.fnal.gov",
                "xrootd.unl.edu"]
    location = "America"
    
    redirectors=[]
    for name in list_names:
        if name in american:
            redirectors.append(name + ":1094")

    redir_raw = []
    for redirector in redirectors[:]:
        redir_info = xrdmapc_list_all_(redirector, global_parent, location)
        redir_raw.append(redir_info)
    return redir_raw

def unify_regional_server_list(region_raw):
    region_in = []
    region_out = []

    for red in region_raw:
        for fullservername in red['names_only']:
            if fullservername[0] != "[":
                region_in.append(fullservername)
                domain = ".".fullservername.split(".")[-3:]
                region_out.append(domain)

    region_in = list(set(region_in))
    region_out = list(set(region_out))
    region_in.sort()
    region_out.sort()

    return region_in, region_out



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

        global_parent = red['name']
        print(global_parent)
        print(red['names_only'])

        print(">>>>  Get EU redirector")
        eu_redir = get_raw_eu_redirectors(global_parent, red['names_only'])
        eu_raw.extend(eu_redir)
        print(">>>>  Get EU redirector: DONE")

        print(">>>>  Get US redirector")
        us_redir = get_raw_us_redirectors(global_parent, red['names_only'])
        us_raw.extend(us_redir)
        print(">>>>  Get US redirector: DONE")

    total_eu_in, total_eu_out = unify_regional_server_list(eu_raw)
    total_us_in, total_us_out = unify_regional_server_list(us_raw)
    