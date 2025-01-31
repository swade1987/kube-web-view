from .resource_registry import ResourceRegistry


class Cluster:
    def __init__(self, name: str, api, labels: dict = None):
        self.name = name
        self.api = api
        self.labels = labels or {}
        self.resource_registry = ResourceRegistry(api)


class ClusterNotFound(Exception):
    def __init__(self, cluster):
        self.cluster = cluster


class ClusterManager:
    def __init__(self, discoverer):
        self._clusters = {}
        self.discoverer = discoverer
        self.reload()

    def reload(self):
        _clusters = {}
        for cluster in self.discoverer.get_clusters():
            _clusters[cluster.name] = Cluster(cluster.name, cluster.api, cluster.labels)

        self._clusters = _clusters

    @property
    def clusters(self):
        return list(self._clusters.values())

    def get(self, cluster: str):
        obj = self._clusters.get(cluster)
        if not obj:
            raise ClusterNotFound(cluster)
        return obj
