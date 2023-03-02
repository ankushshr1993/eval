from django.db import models


# Create your models here.
class Node(models.Model):
    node_name = models.CharField("Node name", max_length=30)
    host_address = models.CharField("Host name", max_length=30)
    host_user = models.CharField("user Id", max_length=30, default="user331828")
    host_cpu = models.FloatField("Measured cpu", default=0)
    host_kf_cpu = models.FloatField("KF cpu", default=0)
    host_kf_cpu_variance = models.FloatField("KF Uncertainty cpu", default=0)

    host_ping = models.FloatField("Ping Value", default=0)
    host_kf_ping = models.FloatField("KF Ping Value", default=0)

    host_enabled = models.BooleanField("Enable host to forward calls", default=True)

    ip_address = models.GenericIPAddressField()
    recent_call = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.node_name


class Experiment(models.Model):
    name = models.CharField("Experiment name", max_length=255)
    description = models.TextField("Experiment description", max_length=255, blank=True)
    n_value = models.IntegerField("Fibonacci n Value", default=5)
    n_nodes = models.IntegerField("Number of enabled Nodes", default=2)
    thread_count = models.IntegerField("Number of thread", default=1)
    filter_enabled = models.BooleanField("Filter enabled/disabled", default=False)
    ping_enabled = models.BooleanField("Ping enabled/disabled", default=False)
    show_plot = models.BooleanField("Show/Hide plot", default=False)

    def __str__(self):
        return "{} [n={}, node={}]".format(self.name, self.n_value, self.n_nodes)


class NodeLogValue(models.Model):
    host_fra_cpu = models.FloatField("Measured cpu Frankfurt", default=0)
    host_fra_kf_cpu = models.FloatField("KF cpu Frankfurt", default=0)
    host_ire_cpu = models.FloatField("Measured cpu Ireland", default=0)
    host_ire_kf_cpu = models.FloatField("KF cpu Ireland", default=0)

    # ping data for logs
    host_fra_ping = models.FloatField("Measured ping Frankfurt", default=0)
    host_fra_kf_ping = models.FloatField("KF ping Frankfurt", default=0)
    host_ire_ping = models.FloatField("Measured ping Ireland", default=0)
    host_ire_kf_ping = models.FloatField("KF ping Ireland", default=0)


class RequestLog(models.Model):
    called_node = models.ForeignKey(Node, on_delete=models.CASCADE)
    called_function = models.CharField("Give function name", max_length=300)
    called_delay = models.FloatField("Function Latency")
    called_url = models.CharField("Url Called", max_length=150)
    called_method = models.CharField("Method", max_length=30, default="GET")
    called_filter = models.CharField("Prediction Type", max_length=30, default="linear")
    measured_cpu = models.FloatField("Measured cpu at call", default=0)
    pred_cpu = models.FloatField("KF cpu at call", default=0)
    pred_cpu_variance = models.FloatField("KF cpu Uncertainty at call", default=0)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, null=True)

    node_data = models.ManyToManyField(NodeLogValue, verbose_name="Nodes Data", blank=True)

    recent_call = models.DateTimeField(auto_now=True)
    reply_call = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.called_function, self.called_node.node_name)
