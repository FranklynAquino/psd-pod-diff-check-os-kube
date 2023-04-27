import subprocess
from time import sleep
import sys
from myUtils import (env, get_logger)
from api.process.opensearch_endpoints import OpenSearchEndpoints
from api.opensearch_response_object import OpenSearchResponseObject


logger = get_logger('Main Run')

def retry_request(instance:OpenSearchEndpoints=None):
    max_tries = 5
    tries = 0
    while tries < max_tries:
        try:
            response = instance.run_search()
            return response
        except Exception as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            sleep(5)
            tries += 1
    logger.info(f'Failed to connect after {max_tries} retries.')
    return None


if len(sys.argv)  < 2:
    numHours = 24
else:
    numHours = int(sys.argv[1])

opensearch_instance = OpenSearchEndpoints(host_name=env.opensearch_host_name,
                                        port_number=env.opensearch_port_number,
                                        opensearch_user=env.opensearch_username,
                                        opensearch_pass=env.opensearch_password)

opensearch_instance.search_setup.set_time_range((numHours*60))

#retry here
results = retry_request(opensearch_instance)

#print(results)
total_aggregations:dict = results['aggregations']
[[key,value]] = total_aggregations.items()

bucket_object_list = []

#kubectl_output = subprocess.check_output("kubectl get pod -o=custom-columns=NAME:.metadata.name --all-namespaces | grep binance  | grep -v balance | grep -v overflow | sort -n > k8slist.csv", shell=True)

#logger.info(f"Your current kubectl response: {kubectl_output.decode('utf8')}")


for aggregations in results['aggregations'][key]['buckets']:
    opensearch_bucket_object = OpenSearchResponseObject()
    opensearch_bucket_object.pod_name = aggregations['key']
    opensearch_bucket_object.doc_count = aggregations['doc_count']
    
    bucket_object_list.append(opensearch_bucket_object)

binance_connector_pod_list = [bucket_object for bucket_object in bucket_object_list 
                            if 'binance' in bucket_object.pod_name]

other_connector_pod_list = [bucket_object for bucket_object in bucket_object_list 
                            if 'binance' not in bucket_object.pod_name]

for bucket_objects in binance_connector_pod_list:
    bucket_objects:OpenSearchResponseObject
    logger.info(f'Soouth-East Binance pods: {bucket_objects.pod_name}')
    
for bucket_objects in other_connector_pod_list:
    bucket_objects:OpenSearchResponseObject
    logger.info(f'Other pods: {bucket_objects.pod_name}')