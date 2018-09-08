import lxml
from lxml import etree
import sys
import os

doc = None
schema = None


def validate_input(data):
    global doc
    global schema
    if doc is None:
        with open("pf_webservice/source/xsd/mspl.xsd") as f:
            doc = etree.parse(f)
        # Schema validation
        try:
            schema = etree.XMLSchema(doc)
        except lxml.etree.XMLSchemaParseError:
            raise Exception("Invalid Schema")

    # Data validation
    doc = etree.fromstring(data)
    try:
        schema.assertValid(doc)
    except lxml.etree.DocumentInvalid:
        raise Exception("Invalid XML Input")

# validate_input('<mspl-set xmlns="http://security.polito.it/shield/mspl"
# xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
# xsi:schemaLocation="http://security.polito.it/shield/mspl
# mspl.xsd"><it-resource id="vNSF2">
# <configuration xsi:type="filtering-configuration">
# <default-action>drop</default-action>
# <resolution-strategy>FMR</resolution-strategy><rule>
# <priority>101</priority><action>reject</action><condition>
# <packet-filter-condition><destination-port>22</destination-port>
# </packet-filter-condition>
# </condition></rule></configuration></it-resource></mspl-set>')
