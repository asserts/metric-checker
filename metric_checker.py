import click
from prometheus.query_client import QueryClient
from pprint import pprint

INSTANT_QUERY = '/api/v1/query?query='

queries = [
    'up',
    'node_uname_info',
    'kubelet_node_name',
    'kube_node_info',
    'count without (cpu, mode)(node_cpu_seconds_total)',
    'count without (instance, container, uid)(kube_pod_owner)',
    'count by(pod, namespace, node)(kube_pod_info)',
    'container_cpu_usage_seconds_total',
]


@click.command()
@click.option('--host', 'host', required=True, envvar='PROMETHEUS_HOST',
              default='http://localhost:9090', help='The prometheus host to query.')
@click.option('--username', 'username', required=False, envvar='PROMETHEUS_USERNAME',
              default='http://localhost:9090', help='The prometheus username')
@click.option('--password', 'password', required=False, envvar='PROMETHEUS_PASSWORD',
              default='http://localhost:9090', help='The prometheus password')
@click.option('--samples', 'samples', required=True, envvar='SAMPLES',
              default=5, help='The number of metrics samples to query via topk().')
def check_metrics(host, username, password, samples):
    client = QueryClient(host, username, password)

    for query in queries:
        if query == 'up':
            endpoint = f'{INSTANT_QUERY}{query}'
        else:
            endpoint = f'{INSTANT_QUERY}topk({samples}, {query})'

        response = client.handle_request(endpoint, 'GET')
        pprint(response)


if __name__ == '__main__':
    check_metrics()