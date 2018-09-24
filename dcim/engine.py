import asyncio
from pysnmp.hlapi.asyncio import (
    nextCmd,
    CommunityData,
    UdpTransportTarget,
    SnmpEngine,
    ContextData,
    ObjectIdentity,
    ObjectType,
    isEndOfMib,
)
from pysnmp.error import PySnmpError
from dcim.core import get_config
import logging

LOGGER = logging.getLogger(__name__)

# asynchronous SNMP walk, steps through each OID at host parameter address
async def async_next_snmp_request(host, *oids):

    snmpEngine = SnmpEngine()

    var_binds = [ObjectType(ObjectIdentity(oid)) for oid in oids]

    while True:
        response = await nextCmd(
            snmpEngine,
            CommunityData(get_config('snmp')['COMM_STRING'], mpModel=1),
            UdpTransportTarget((host, 161)),
            ContextData(),
            *var_binds,
        )

        error_indication, error_status, error_index, varbind_table = response

        if error_indication:
            LOGGER.warning('%s with this asset: %s', error_indication, host)
            return

        elif error_status:
            LOGGER.warning(
                '%s at %s',
                error_status.prettyPrint(),
                error_index and varbind_table[-1][int(error_index) - 1] or '?'
            )
            return

        else:
            var_binds = varbind_table[-1]
            if isEndOfMib(var_binds):
                return

            print(varbind_table)


def test():
    # test parameters for live SNMP targets
    hostname = 'demo.snmplabs.com'
    oids = [
        '1.3.6.1',
        '1.3.6.1.4.1.13742.6.5.5.3.1.4.1',
        '1.3.6.1.4.1.13742.6.3.6.3.1.2.1',
    ]

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            async_next_snmp_request(hostname, *oids)
        )
    ]

    result = loop.run_until_complete(
        asyncio.wait(
            tasks,
            loop=loop,
        )
    )
    return result


def async_process_equipment(equipment):
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            async_next_snmp_request(equipment.ip, *equipment.oid_array)
        )
    ]

    result = loop.run_until_complete(
        asyncio.wait(
            tasks,
            loop=loop,
        )
    )
    return result
