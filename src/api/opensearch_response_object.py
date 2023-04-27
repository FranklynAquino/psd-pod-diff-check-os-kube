class OpenSearchResponseObject:
    def __init__(self, public_ip=None, pod_name=None, doc_count=None):
        self.public_ip = public_ip
        self.pod_name = pod_name
        self.doc_count = doc_count
        
        
    def __str__(self):
        return (f'OpenSearch Object\nPublic IP: {self.public_ip}\nPod Name: {self.pod_name}\nDoc Count: {self.doc_count}\n')