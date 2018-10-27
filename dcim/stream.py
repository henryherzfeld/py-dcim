from walrus import *
from dcim.configuration import get_config


class StreamEngine:
    stream = 0

    def __init__(self):
        stream_config = get_config('db')
        host = stream_config['DB_HOST']

        db = Database(
            host=host,
            port=6379,
            db=0
        )
        self.stream = db.Stream('stream1')

    def add(self, data):
        for item in data:
            if item:
                for oid, payload in data:
                    self.stream.add({payload: data})

        data.clear()
