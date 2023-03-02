from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('latency/', views.time_latency, name='time_latency'),
    path('latency/<int:eid>', views.time_latency, name='time_latency'),
    path('api/v1/namespaces/_/actions/fib',
         views.serverless_call, name='function'),
    path('api/v1/namespaces/_/actions/pyfib',
         views.serverless_call, name='py_function'),

]
