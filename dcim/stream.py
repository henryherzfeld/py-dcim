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
        for request_data, metadata in data:
            if request_data:
                self.stream.add({request_data: metadata})
