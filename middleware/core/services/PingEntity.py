# ping resource parsed for value and saved according to host.

class PingEntity(object):

    def __init__(self, host, resource_type, value):
        self.host = host
        self.rawResourceType = resource_type
        self.rawValue = value
        self.parse_ping_value()
        self.date_time = self.get_date_time()
        self.usage = self.get_ping_usage()

    def parse_ping_value(self):
        self.rawValue = self.rawValue.split(':')

    def get_date_time(self):
        return float(self.rawValue[0])

    def get_ping_usage(self):
        return float(self.rawValue[1])

    def to_dict(self):
        return {'host': self.host, 'type': self.rawResourceType, 'time': self.date_time,
                'usage': self.usage}
