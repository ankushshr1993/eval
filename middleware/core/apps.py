from django.apps import AppConfig

# The callback for when the client receives a CONNACK response from the server.
from core.services.MQTTService import MQTTService


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from .models import Node
        client = MQTTService(client_id="middleware")
        rc = client.run()
        print("rc: " + str(rc))
