import xmltodict
import pf
import socket
from common import settings


def xml_to_pfrule(data):
    print "starting translation"
    print data
    xml_datas = []
    xml_rules = xmltodict.parse(
        data,
        dict_constructor=dict)["mspl-set"]["it-resource"]["configuration"]["rule"]
    if isinstance(xml_rules, list):
        for xml_rule in xml_rules:
            xml_datas.append(xml_rule)
    else:
        xml_datas.append(xml_rules)

    rate_limit = None
    rules = pf.PFRuleset()

    for xml_data in xml_datas:
        print xml_data
        rule = pf.PFRule()
        if settings.quick_rules == "True":
            rule.quick = True
        Addrs = None
        Addrd = None
        Ports = None
        Portd = None
        
        xml_src = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"], "source-address")
        if xml_src is not None:
            Addrs = pf.PFAddr(xml_src)

        xml_dst = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"],
            "destination-address")
        if xml_dst is not None:
            Addrd = pf.PFAddr(xml_dst)
        
        xml_proto = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"],
            "protocol")
        print xml_proto.lower()
        if xml_proto is not None:
            if xml_proto.lower() == "tcp":
                rule.proto = socket.IPPROTO_TCP
            elif xml_proto.lower() == "udp":
                rule.proto = socket.IPPROTO_UDP
 
        xml_direction = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"],
            "direction")
        if xml_direction is not None:
            if xml_direction.lower() == "inbound":
                rule.direction = pf.PF_IN
            elif xml_direction.lower() == "outbound":
                rule.direction = pf.PF_OUT
        
        xml_interface = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"],
            "interface")
        if xml_interface is not None:
            rule.ifname = xml_interface

        xml_sport = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"], "source-port")
        xml_dport = getValIfKeyExists(
            xml_data["condition"]["packet-filter-condition"],
            "destination-port")
        
        # Retrieve default target from MSPL
        default_target = getValIfKeyExists(xml_data, "action").upper()
        if default_target is not None:
            if default_target == "ACCEPT":
                rule.action = pf.PF_PASS
                rule.keep_state = pf.PF_STATE_NORMAL
            elif default_target == "DROP" or default_target == "REJECT":
                rule.action = pf.PF_DROP
                if default_target == "REJECT":
                    rule.rule_flag = pf.PFRULE_RETURN

        # In case of packets/sec rate limit:
        if getValIfKeyExists(
                xml_data["condition"],
                "traffic-flow-condition") is not None:

            # It is a number of allowed packets or bits per unit of time
            # (seconds, minutes, hours or days).
            # -m limit --limit <rate-limit> --limit-burst <limit-burst> \
            # -j ACCEPT
            #rate_limit = getValIfKeyExists(
            #    xml_data["condition"]["traffic-flow-condition"],
            #    "rate-limit")

            # The maximum number of connections per host.
            max_connections = getValIfKeyExists(
                xml_data["condition"]["traffic-flow-condition"],
                "max-connections")
            # If the action is DROP or REJECT the rule will fire an error if max_src_conn is setted
            if max_connections is not None and default_target == "ACCEPT":
                print "Setted maxconn"
                #rule.max_src_nodes = max_connections
                rule.max_src_conn = max_connections
                rule.max_src_states = max_connections

        # In case of specified ports:
        if xml_sport is not None:
            if xml_proto is not None:
                if xml_proto.lower() == "tcp":
                    Ports = pf.PFPort(xml_sport, socket.IPPROTO_TCP)
                elif xml_proto.lower() == "udp":
                    Ports = pf.PFPort(xml_sport, socket.IPPROTO_UDP)
            elif xml_proto is None:
                Ports = pf.PFPort(xml_sport)
        if xml_dport is not None:
            if xml_proto is not None:
                if xml_proto.lower() == "tcp":
                    Portd = pf.PFPort(xml_dport, socket.IPPROTO_TCP)
                elif xml_proto.lower() == "udp":
                    Portd = pf.PFPort(xml_dport, socket.IPPROTO_UDP)
            elif xml_proto is None:
                Portd = pf.PFPort(xml_dport)

        # TODO: Manage Priority
        priority = getValIfKeyExists(xml_data, "priority")
        
        if Addrs is not None and Ports is not None:
            rule.src = pf.PFRuleAddr(Addrs, Ports)
        elif Addrs is not None:
            rule.src = pf.PFRuleAddr(Addrs)
        elif Ports is not None:
            rule.src = pf.PFRuleAddr(Ports)

        if Addrd is not None and Portd is not None:
            rule.dst = pf.PFRuleAddr(Addrd, Portd)
        elif Addrd is not None:
            rule.dst = pf.PFRuleAddr(Addrd)
        elif Portd is not None:
            rule.dst = pf.PFRuleAddr(Portd) 
        # Append rule
        rules.append(rule)

    return rules


def getValIfKeyExists(dict_var, key_var):
    if key_var in dict_var:
        return dict_var[key_var]
    else: 
        if key_var[-5:] == "_list":
            return []
        else:
            return None
