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
        stream_config = get_config('db')
        packet_size = stream_config['DB_PACKET']

        packet = []

        for index, item in enumerate(data):
            for oid, payload in data:
                entry = {payload: data}
                packet.append(entry)

            if index == packet_size:
                self.stream.add({0: packet})
                packet.clear()

        data.clear()
