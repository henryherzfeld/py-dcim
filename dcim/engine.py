from pysnmp.error import PySnmpError
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
from pysnmp.smi import view
import asyncio
import logging
from collections import defaultdict
from dcim.configuration import get_config


LOGGER = logging.getLogger(__name__)


# Adaption of PySNMP Engine, performs all SNMP processing asynchronously
class Engine:
    requests = []
    targets = []
    results = []
    community_string = ''
    timeout = 0
    snmpEngine = 0
    loop = 0
    queue = 0
    mibViewController = 0

    def __init__(self, targets):
        self.requests = []
        self.targets = targets
        self.results = []
        self.community_string = get_config('snmp')['COMM_STRING']
        self.timeout = get_config('snmp')['TIMEOUT']
        self.snmpEngine = SnmpEngine()
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.mibViewController = view.MibViewController(self.snmpEngine.getMibBuilder())

        #self.test()

    # asynchronous SNMP walk, steps through each OID at host parameter address
    async def next_snmp_request(self, host, *oids):

        print("attempting SNMP for " + host)

        for oid in oids:
            var_bind = ObjectType(ObjectIdentity('POWERNET-MIB', oid).addAsn1MibSource('http://mibs.snmplabs.com/asn1/@mib@'))

            var_bind.resolveWithMib(self.mibViewController)

            while True:
                response = await nextCmd(
                    self.snmpEngine,
                    CommunityData(self.community_string, mpModel=1),
                    UdpTransportTarget((host, 161)),
                    ContextData(),
                    var_bind,
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

                    print(varbind_table)

    # retrieves snmp data from each target's equipment, builds and sorts dictionary of lists
    # where key is ip and value is array of all oids, stores request calls for each ip in event loop
    def enqueue_requests(self):
        print('enqueueing requests')

        request_data_sorted = defaultdict(lambda: 0)

        for target in self.targets:
            request_data = target.get_equipment_snmp_data()

            for ip in request_data:
                request_data_sorted[ip] = (request_data[ip])

        for ip, oid_array in request_data_sorted.items():
            self.requests.append(
                self.loop.create_task(
                    self.next_snmp_request(ip, *oid_array)
                )
            )

    def process_requests(self):
        print('processing request queue')
        results = list

        results.append([self.loop.run_until_complete(self.process_request(request)) for request in self.requests])
        
        return results

    async def process_request(self, task):

        result = await asyncio.wait_for(
                        asyncio.shield(task),
                        self.timeout,
                        loop=self.loop,
        )

        return result

    def test(self):
        # test parameters for live SNMP targets
        hostname = 'demo.snmplabs.com'
        oids = [
            'airIRRP100UnitStatusRackInletTempMetric',
        ]
        community_string = 'public'

        print('performing test for: {0} oids at '.format(len(oids)) + hostname)

        tasks = [
            self.loop.create_task(
                self.next_snmp_request(hostname, *oids)
            )
        ]

        result = self.loop.run_until_complete(
            asyncio.wait(
                tasks,
                loop=self.loop,
            )
        )
        return result