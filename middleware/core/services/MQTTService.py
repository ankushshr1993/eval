import threading
import time
# import the logging library
import logging

from django.conf import settings
import paho.mqtt.subscribe as subscribe

from core.services.CPUEntity import CPUEntity
from core.services.KLFilter import KLFilter

# Get an instance of a logger
from core.services.PingEntity import PingEntity

logger = logging.getLogger(__name__)


class MQTTService():  # mqtt.Client
    topic = "collectd/#"
    host = "middleware.lifemachine.net"  # "broker.hivemq.com"  # "localhost"
    resources = ['cpu', 'ping']
    kl_cpu_frankfurt = None
    kl_cpu_ireland = None

    kl_ping_frankfurt = None
    kl_ping_ireland = None

    def __init__(self, client_id):
        self.client_id = client_id
        self.host = settings.MQTT_BROKER_URL
        self.port = settings.MQTT_BROKER_PORT
        self.topic = settings.MQTT_TOPIC_COLLECTD
        self.kl_cpu_frankfurt = KLFilter()
        self.kl_cpu_ireland = KLFilter()
        self.kl_ping_frankfurt = KLFilter()
        self.kl_ping_ireland = KLFilter()

    def on_message(self, mqttc, obj, msg):
        if any(x in msg.topic for x in self.resources):
            # data abstraction from response
            (prefix, host, resource, sub_type) = tuple(msg.topic.split('/'))
            # print(prefix+":"+host+":"+resource+":"+sub_type)
            if 'middleware' not in host:
                # payload decoding, Plain Text Protocol from collectd
                decoded_msg = msg.payload.decode('ascii').strip().strip('\x00')
                # logger.info(prefix + ":" + host + ":" + resource + ":" + sub_type + "\t" + str(decoded_msg))
                if 'cpu' in resource and 'percent-user' in sub_type:
                    if 'frankfurt' in host:
                        #logger.info('KL Frankfurt')
                        # subtract 50 and scale to 100%
                        cpu_resource = CPUEntity(host, sub_type, decoded_msg, 50)
                        self.kl_calculation(self.kl_cpu_frankfurt, cpu_resource, host)
                    else:
                        #logger.info('KL Ireland')
                        cpu_resource = CPUEntity(host, sub_type, decoded_msg)
                        self.kl_calculation(self.kl_cpu_ireland, cpu_resource, host)
            else:
                if 'ping' in resource:
                    if 'ping-frankfurt' in sub_type:
                        decoded_msg = msg.payload.decode('ascii').strip().strip('\x00')
                        #logging.info(decoded_msg)
                        ping_resource = PingEntity("frankfurt.lifemachine.net", sub_type, decoded_msg)
                        self.kl_ping_calculation(self.kl_ping_frankfurt, ping_resource)
                        #logger.warning(ping_resource.to_dict())

                    if 'ping-ireland' in sub_type:
                        decoded_msg = msg.payload.decode('ascii').strip().strip('\x00')
                        #logging.info(decoded_msg)

                        ping_resource = PingEntity("ireland.lifemachine.net", sub_type, decoded_msg)
                        self.kl_ping_calculation(self.kl_ping_ireland, ping_resource)
                        #logger.warning(ping_resource.to_dict())


    def set_callback(self):
        subscribe.callback(self.on_message, self.topic, hostname=f"{self.host}", client_id=self.client_id)

    def run(self):
        logger.info(self.host + ":" + str(self.port))

        x = threading.Thread(target=self.set_callback)
        logging.info("MQTT SERVICE    :Runnign Callback in Thread")
        x.start()

    # CPU filter calculation
    def kl_calculation(self, kl_fun, cpu_resource, host):
        kl_fun_v = kl_fun.run_filter(cpu_resource.get_cpu_usage())
        logger.info(cpu_resource.__dict__)
        try:
            from core.models import Node
            node = Node.objects.get(host_address=host)
            node.host_cpu = cpu_resource.get_cpu_usage()
            node.host_kf_cpu = kl_fun_v[0]
            node.host_kf_cpu_variance = kl_fun_v[1]
            node.save()
        except:
            pass

    # ping filter calculation
    def kl_ping_calculation(self, kl_fun, ping_resource):
        kl_fun_v = kl_fun.run_filter(ping_resource.get_ping_usage())
        logger.info(ping_resource.__dict__)
        try:
            from core.models import Node
            node = Node.objects.get(host_address=ping_resource.host)
            node.host_ping = ping_resource.get_ping_usage()
            node.host_kf_ping = kl_fun_v[0]
            node.save()
        except:
            pass
