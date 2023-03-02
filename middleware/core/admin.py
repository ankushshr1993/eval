from django.contrib import admin

# Register your models here.
from core.models import Node, RequestLog, Experiment, NodeLogValue


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "node_name", "host_address", "host_user", "ip_address", "host_cpu",
        "host_kf_cpu", 'host_ping', 'host_kf_ping', 'recent_call', 'host_enabled')


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = (
        "id", "called_node", "called_function", "called_delay", "called_method", "called_filter", "experiment")


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "n_value", "n_nodes", "filter_enabled","ping_enabled", "show_plot", 'thread_count')


@admin.register(NodeLogValue)
class NodeLogValueAdmin(admin.ModelAdmin):
    list_display = (
    "id", "host_fra_cpu", "host_fra_kf_cpu", "host_ire_cpu", "host_ire_kf_cpu", "host_fra_ping", "host_fra_kf_ping",
    "host_ire_ping", "host_ire_kf_ping")
