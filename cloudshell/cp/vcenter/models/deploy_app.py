from cloudshell.cp.core.request_actions.models import DeployApp
from cloudshell.shell.standards.core.resource_config_entities import (
    ResourceAttrRO,
    ResourceBoolAttrRO,
)

from cloudshell.cp.vcenter import constants


class ResourceAttrRODeploymentPath(ResourceAttrRO):
    def __init__(self, name, namespace="DEPLOYMENT_PATH"):
        super().__init__(name, namespace)


class ResourceBoolAttrRODeploymentPath(ResourceBoolAttrRO):
    def __init__(self, name, namespace="DEPLOYMENT_PATH", *args, **kwargs):
        super().__init__(name, namespace, *args, **kwargs)


class BaseVCenterDeployApp(DeployApp):
    vm_cluster = ResourceAttrRODeploymentPath("VM Cluster")
    vm_storage = ResourceAttrRODeploymentPath("VM Storage")
    vm_resource_pool = ResourceAttrRODeploymentPath("VM Resource Pool")
    vm_location = ResourceAttrRODeploymentPath("VM Location")
    behavior_during_save = ResourceAttrRODeploymentPath("Behavior during save")
    auto_power_on = ResourceBoolAttrRODeploymentPath("Auto Power On")
    auto_power_off = ResourceBoolAttrRODeploymentPath("Auto Power Off")
    wait_for_ip = ResourceBoolAttrRODeploymentPath("Wait for IP")
    auto_delete = ResourceBoolAttrRODeploymentPath("Auto Delete")
    autoload = ResourceBoolAttrRODeploymentPath("Autoload")
    ip_regex = ResourceAttrRODeploymentPath("IP Regex")
    refresh_ip_timeout = ResourceAttrRODeploymentPath("Refresh IP Timeout")


class VMFromVMDeployApp(BaseVCenterDeployApp):
    DEPLOYMENT_PATH = constants.VM_FROM_VM_DEPLOYMENT_PATH
    vcenter_vm = ResourceAttrRODeploymentPath("vCenter VM")


class VMFromTemplateDeployApp(BaseVCenterDeployApp):
    DEPLOYMENT_PATH = constants.VM_FROM_TEMPLATE_DEPLOYMENT_PATH
    vcenter_template = ResourceAttrRODeploymentPath("vCenter Template")


class VMFromLinkedCloneDeployApp(BaseVCenterDeployApp):
    DEPLOYMENT_PATH = constants.VM_FROM_LINKED_CLONE_DEPLOYMENT_PATH
    vcenter_vm = ResourceAttrRODeploymentPath("vCenter VM")
    vcenter_vm_snapshot = ResourceAttrRODeploymentPath("vCenter VM Snapshot")


class VMFromImageDeployApp(BaseVCenterDeployApp):
    DEPLOYMENT_PATH = constants.VM_FROM_IMAGE_DEPLOYMENT_PATH
    vcenter_image = ResourceAttrRODeploymentPath("vCenter Image")
    vcenter_image_arguments = ResourceAttrRODeploymentPath("vCenter Image Arguments")
