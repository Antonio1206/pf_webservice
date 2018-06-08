import pffunction
import mspl_translator
import os.path
import json

def add_rules(payload):
    rules = mspl_translator.xml_to_pfrule(payload)
    if os.path.isfile("osmconfig"):
        with open("checkrules","a") as check:
            check.write(str(rules))
            check.write('\n')
        try:
            pfctl("-n -f checkrules")
        except Exception as error:
            os.remove("checkrules")
            raise Exception("Unable to add rules due to rules integrity error")
        os.remove("checkrules")
        with open("osmconfig","a") as f:
            f.write(str(rules))
            f.write('\n')
    else:
        with open("osmconfig","w") as newf:
            newf.write(str(rules))
            newf.write('\n')   
    pffunction.pfctl("-a osmrules -f osmconfig")

def delete_rules():
    if os.path.isfile("osmconfig"):
        os.remove("osmconfig")
    pffunction.pfctl("-a osmrules -F rules")

def remove_single_rule(line_number):
    if os.path.isfile("osmconfig"):
        os.rename("osmconfig","tmposmconfig")
        line_to_erase = [int(line_number)]
        with open("tmposmconfig", 'r') as fin, open("osmconfig", 'w') as fout:
            for lineno, line in enumerate(fin, 1):
                if lineno not in line_to_erase:
                    fout.write(line)
        os.remove("tmposmconfig")
    pffunction.pfctl("-a osmrules -f osmconfig")

def get_json_rules():
    if os.path.isfile("osmconfig"):
        json_result = {}
        i = 0
        with open("osmconfig",'r') as f:
            for line in f:
               json_rule = get_rule_dict(line)
               if json_rule is not None:
                   json_result[i] = json_rule
                   i += 1
        
        return json_result    
    else:
        return None
    
def get_rule_dict(rule):
    quick = "False"
    src = None
    dst = None
    protocol = None
    interface = None
    sport = None
    dport = None
    direction = None
    connlimit = None
    action = None
    connrate = None
    policy_found = False
    tmprule = rule.split(" ")
    i = 0
    while i < len(tmprule):
        
        #Read the action
        if tmprule[i] == "pass":
            action = "accept"
            policy_found = True
        elif tmprule[i] == "block":
            i += 1
            policy_found = True
            if tmprule[i] == "drop":
                action = "drop"
            else:
                action = "reject"
        elif tmprule[i] == "scrub":
            action = "scrub"
            policy_found = True

        #Read the direction if exists
        elif tmprule[i] == "in":
            direction = "inbound"
        elif tmprule[i] == "out":
            direction = "outbound"
 
        #Read quick keywork if exists
        elif tmprule[i] == "quick":
            quick = "True"
        #Read interface if exists
        elif tmprule[i] == "on":
            i += 1
            interface = tmprule[i].replace("vtnet","eth")        

        #Read the protocol if exists
        elif tmprule[i] == "proto":
            i += 1
            protocol = tmprule[i]

        #Read the source
        elif tmprule[i] == "from":
            i += 1
            #If the value is "=" only if the port is specified without a specific source
            if tmprule[i] == "=":
                src = "any"
                i += 1
                sport = tmprule[i]
            else:
                src = tmprule[i]
                i += 1
                #Read sport if exist
                if tmprule[i] == "port":
                    i += 2             #Jump the char "="
                    sport = tmprule[i]
                else:
                    continue

        #Read the destination
        elif tmprule[i] == "to":
            i += 1
            #If the value is "=" only the port is specified
            if tmprule[i] == "=":
                dst = "any"
                i += 1
                dport = tmprule[i].strip('\n')
            else:
                dst = tmprule[i].strip('\n')
                i += 1
                if i >= len(tmprule):
                    break
                #Read sport if exist
                if tmprule[i] == "port":
                    i += 2             #Jump the char "="
                    dport = tmprule[i].strip('\n')
                else:
                    continue

        #Read max-connections if exists
        elif tmprule[i] == "max-src-conn":
            i += 1
            connlimit = tmprule[i].strip(")\n")
        
        #Read connections-limit if exists
        elif tmprule[i] == "max-src-conn-rate":
            i += 1
            connrate = tmprule[i].strip(")\n")
        #Increment i and continue the cycle
        i += 1
    
    # END OF WHILE CYCLE    
    # Now my variables are ready for build a JSON

    if policy_found == False:
        return None    

    json_rule = {
        "action": action,
        "src": src,
        "dst": dst,
        "quick" : quick
    }
    if direction is not None:
        json_rule['direction'] = direction
    if protocol is not None:
        json_rule['protocol'] = protocol
    if interface is not None:
        json_rule['interface'] = interface
    if sport is not None:
        json_rule['source-port'] = sport
    if dport is not None:
        json_rule['destination-port'] = dport
    if connlimit is not None:
        json_rule['max connections'] = connlimit
    if connrate is not None:
        json_rule['connections rate'] = connrate    

    return json_rule
