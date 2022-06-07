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
@click.option('--host', 'host', required=True,
              default='http://localhost:9090', help='The prometheus host to query.')
@click.option('--samples', 'samples', required=True,
              default=5, help='The number of metrics samples to query via topk().')
def check_metrics(host, samples):
    client = QueryClient(host)

    for query in queries:
        endpoint = f'{INSTANT_QUERY}topk({samples}, {query})'
        response = client.handle_request(endpoint, 'GET')
        pprint(response)


if __name__ == '__main__':
    check_metrics()