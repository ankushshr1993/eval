# memory resource parsed for value and saved according to host.

class MemoryEntity(object):

    def __init__(self, host, resource_type, value):
        self.host = host
        self.rawResourceType = resource_type
        self.rawValue = value
        self.parse_memory_value()
        self.date_time = self.get_date_time()
        self.usage = self.get_memory_usage()

    def parse_memory_value(self):
        self.rawValue = self.rawValue.split(':')

    def get_date_time(self):
        return float(self.rawValue[0])

    def get_memory_usage(self):
        return float(self.rawValue[1])

    def to_dict(self):
        return {'host': self.host, 'type': self.rawResourceType, 'time': self.date_time,
                'usage': self.usage}

