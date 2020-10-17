from cloudshell.cp.core.request_actions.models import DeployApp
from cloudshell.shell.standards.core.resource_config_entities import ResourceAttrRO


class ResourceAttrRODeploymentPath(ResourceAttrRO):
    def __init__(self, name, namespace="DEPLOYMENT_PATH"):
        super().__init__(name, namespace)


class BaseVCenterDeployApp(DeployApp):
    pass
