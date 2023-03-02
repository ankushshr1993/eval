# cpu resource parsed for value and saved according to host.

class CPUEntity(object):

    def __init__(self, host, resource_type, value, scale=0):
        self.host = host
        self.rawResourceType = resource_type
        self.rawValue = value
        self.scale = scale
        self.parse_cpu_value()
        self.date_time = self.get_date_time()
        self.usage = self.get_cpu_usage()

    def parse_cpu_value(self):
        self.rawValue = self.rawValue.split(':')

    def get_date_time(self):
        return float(self.rawValue[0])

    def get_cpu_usage(self):
        if self.scale > 0:
            # (x - scale) x 2
            print("{} Scaled to :{}".format(float(self.rawValue[1]), (float(self.rawValue[1])-self.scale)*2 ))
            return (float(self.rawValue[1])-self.scale)*2
        return float(self.rawValue[1])

    def to_dict(self):
        return {'host': self.host, 'type': self.rawResourceType, 'time': self.date_time,
                'usage': self.usage}
