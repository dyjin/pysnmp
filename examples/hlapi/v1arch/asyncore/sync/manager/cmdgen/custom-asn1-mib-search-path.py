"""
Custom ASN.1 MIB path
+++++++++++++++++++++

Send SNMP GET request using the following options:

* with SNMPv2c, community 'public'
* over IPv4/UDP
* to an Agent at demo.snmplabs.com:161
* for IF-MIB::ifInOctets.1 MIB object
* pass non-default ASN.1 MIB source to MIB compiler
* with MIB lookup enabled

Functionally similar to:

| $ snmpget -v2c -c public -M /usr/share/snmp demo.snmplabs.com IF-MIB::ifInOctets.1

"""#
from pysnmp.hlapi.v1arch import *

iterator = getCmd(
    SnmpDispatcher(),
    CommunityData('public'),
    UdpTransportTarget(('demo.snmplabs.com', 161)),
    ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 1).addAsn1MibSource(
        'file:///usr/share/snmp',
        'http://mibs.snmplabs.com/asn1/@mib@')
    ),
    lookupMib=True
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
