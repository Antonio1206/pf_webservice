IPADDR=localhost
PORT=9999
RULE_ID=1

set-policies:
	curl -X POST -d '<mspl-set xmlns="http://security.polito.it/shield/mspl" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://security.polito.it/shield/mspl mspl.xsd"><it-resource id="vNSF2"><configuration xsi:type="filtering-configuration"><default-action>drop</default-action><resolution-strategy>FMR</resolution-strategy><rule><priority>101</priority><action>reject</action><condition><packet-filter-condition><destination-port>22</destination-port></packet-filter-condition></condition></rule></configuration></it-resource></mspl-set>' http://${IPADDR}:${PORT}/setRules/v1
