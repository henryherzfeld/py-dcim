from walrus import *
from dcim.configuration import get_config


class StreamEngine:
    stream = 0


    def __init__(self):
        stream_config = get_config('db')
        host = stream_config['DB_HOST']
        password = stream_config['DB_PASS']

        db = Database(
            host=host,
            port=6379,
            password=password,
            db=0
        )
        self.stream = db.Stream('stream2')

    def add(self, data):
        failures = 0
        for item in data:
            if item:
                for oid, payload in data:
                    self.stream.add({payload: data})

            else:
                failures += 1

        if failures:
            print('{0} snmp attempts not sent to stream'.format(failures))

        data.clear()
