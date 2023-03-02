# import random
import json

from django.db.models import Avg, Max, Min, Sum, F
from django.db import models
from django.http import HttpResponse, JsonResponse
import requests as req
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from core.models import Node, RequestLog, Experiment, NodeLogValue


def index(request):
    # log_data_set = RequestLog.objects.values('recent_call', 'called_delay').order_by('recent_call')[:5]
    # graph_dataset = [data.values() for data in list(log_data_set)]
    # context = {'time_latency': graph_dataset}

    experiments = Experiment.objects.filter(show_plot=True).order_by("id").reverse()
    context = {'experiments': experiments}
    return render(request, "home.html", context)


def time_latency(request, eid):
    log_data_set = RequestLog.objects.filter(experiment_id=eid).values('recent_call', 'called_delay', 'measured_cpu',
                                                                       'pred_cpu',
                                                                       'node_data__host_fra_cpu',
                                                                       'node_data__host_ire_cpu',
                                                                       'node_data__host_fra_kf_cpu',
                                                                       'node_data__host_ire_kf_cpu',

                                                                       'node_data__host_fra_ping',
                                                                       'node_data__host_ire_ping',
                                                                       'node_data__host_fra_kf_ping',
                                                                       'node_data__host_ire_kf_ping'
                                                                       ).order_by(
        'recent_call')
    latency = []
    measured_cpu = []
    prediction_cpu = []
    host_fra_cpu = []
    host_ira_cpu = []
    pred_host_fra_cpu = []
    pred_host_ira_cpu = []

    host_fra_ping = []
    host_ira_ping = []
    pred_host_fra_ping = []
    pred_host_ira_ping = []

    for item in list(log_data_set):
        latency.append([item['recent_call'], item['called_delay']])
        measured_cpu.append([item['recent_call'], item['measured_cpu']])
        prediction_cpu.append([item['recent_call'], item['pred_cpu']])

        host_fra_cpu.append([item['recent_call'], item['node_data__host_fra_cpu']])
        host_ira_cpu.append([item['recent_call'], item['node_data__host_ire_cpu']])

        pred_host_fra_cpu.append([item['recent_call'], item['node_data__host_fra_kf_cpu']])
        pred_host_ira_cpu.append([item['recent_call'], item['node_data__host_ire_kf_cpu']])

        host_fra_ping.append([item['recent_call'], item['node_data__host_fra_ping']])
        host_ira_ping.append([item['recent_call'], item['node_data__host_ire_ping']])
        pred_host_fra_ping.append([item['recent_call'], item['node_data__host_fra_kf_ping']])
        pred_host_ira_ping.append([item['recent_call'], item['node_data__host_ire_kf_ping']])

    avg_delay = RequestLog.objects.filter(experiment_id=eid).aggregate(Avg('called_delay'))
    avg_measured_cpu = RequestLog.objects.filter(experiment_id=eid).aggregate(Avg('measured_cpu'))
    avg_pred_cpu = RequestLog.objects.filter(experiment_id=eid).aggregate(Avg('pred_cpu'))

    max_delay = RequestLog.objects.filter(experiment_id=eid).aggregate(Max('called_delay'))
    min_delay = RequestLog.objects.filter(experiment_id=eid).aggregate(Min('called_delay'))

    graph_dataset = {'avg_delay': avg_delay['called_delay__avg'],
                     'max_delay': max_delay['called_delay__max'],
                     'min_delay': min_delay['called_delay__min'],
                     'avg_measured_cpu': avg_measured_cpu['measured_cpu__avg'],
                     'avg_pred_cpu': avg_pred_cpu['pred_cpu__avg'],
                     'latency': latency,
                     'fra_cpu': host_fra_cpu,
                     'ire_cpu': host_ira_cpu,
                     'pred_fra_cpu': pred_host_fra_cpu,
                     'pred_ira_cpu': pred_host_ira_cpu,

                     'fra_ping': host_fra_ping,
                     'ire_ping': host_ira_ping,
                     'pred_fra_ping': pred_host_fra_ping,
                     'pred_ira_ping': pred_host_ira_ping,

                     'mes_cpu': measured_cpu,
                     'pred_cpu': prediction_cpu}
    return JsonResponse(graph_dataset, safe=False)


@csrf_exempt
def serverless_call(request):
    # get first host possible
    experiment_id = request.GET.get('exp', 1)
    experiment = Experiment.objects.get(id=experiment_id)
    print("\nSelected Experiment\n")
    print(experiment)
    if experiment.filter_enabled and experiment.ping_enabled:
        # adds ping to the filter result to get appropriate node.
        filter_type = "kf_cpu_ping"
        node = Node.objects.filter(host_enabled=True).annotate(amount=Sum(F('host_ping') +
                                                                          F('host_kf_cpu'),
                                                                          output_field=models.FloatField())).order_by(
            'amount').first()

    elif experiment.filter_enabled and not experiment.ping_enabled:
        filter_type = "kf_cpu"
        node = Node.objects.order_by('host_kf_cpu').filter(host_enabled=True).first()
    else:
        filter_type = "cpu"
        node = Node.objects.order_by('host_cpu').filter(host_enabled=True).first()

    # extract request and log-info from host
    current_recommended_host = node.host_address
    current_measured_cpu = node.host_cpu
    current_pred_cpu = node.host_kf_cpu
    current_pred_cpu_var = node.host_kf_cpu_variance
    function_request_url = "https://{}{}?{}".format(current_recommended_host, request.path,
                                                    "blocking=true&result=true")
    print("\nrequest Uri\n")
    print(request.get_raw_uri())
    print("\n Function request Uri for POST\n")
    print(function_request_url)

    headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive', 'Cache-Control': 'no-cache',
               'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A='}

    print("\n Header, type, request body\n-----------------------------")
    print(request.headers)
    print(filter_type)
    print(request.body)

    n_value_dict = {'n': experiment.n_value}
    req_body = json.dumps(n_value_dict)
    print("\n N value to send\n-----------------------------")
    print(req_body)

    function_response = req.post(function_request_url, data=req_body, headers=headers,
                                 verify=False, timeout=15)

    # save in analytics in db
    if function_response.status_code == 200:
        print("\nFunction Response from Node\n-----------------------------")
        print(function_response.content)
        request_log = RequestLog(called_node=node, called_function="fib",
                                 called_delay=function_response.elapsed.total_seconds(),
                                 called_url=function_response.url,
                                 called_method=request.method, called_filter=filter_type,
                                 measured_cpu=current_measured_cpu, pred_cpu=current_pred_cpu,
                                 pred_cpu_variance=current_pred_cpu_var, experiment=experiment)
        print(function_response.elapsed.total_seconds())
        q = Node.objects.order_by('id').values('host_cpu', 'host_kf_cpu', 'host_ping', 'host_kf_ping')
        # print(q)

        request_log.save()
        if q.count() >= 2:
            nod_val = NodeLogValue(
                host_fra_cpu=q[0]['host_cpu'], host_ire_cpu=q[1]['host_cpu'],
                host_fra_kf_cpu=q[0]['host_kf_cpu'], host_ire_kf_cpu=q[1]['host_kf_cpu'],

                host_fra_ping=q[0]['host_ping'], host_ire_ping=q[1]['host_ping'],
                host_fra_kf_ping=q[0]['host_kf_ping'], host_ire_kf_ping=q[1]['host_kf_ping'],
            )
            nod_val.save()
            request_log.node_data.add(nod_val)
            request_log.save()
        # print(function_response.content)

    return HttpResponse(
        "called n= %s function  %s %s %s %s" % (experiment.n_value, function_request_url, function_response.status_code,
                                                function_response.content,
                                                function_response.elapsed.total_seconds()))
