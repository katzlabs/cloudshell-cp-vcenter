from __future__ import annotations

from cloudshell.cp.core.request_actions.models import DeployApp

from cloudshell.cp.vcenter import constants
from cloudshell.cp.vcenter.models.base_deployment_app import (
    HddSpecsAttrRO,
    ResourceAttrRODeploymentPath,
    ResourceBoolAttrRODeploymentPath,
    ResourceFloatAttrRODeploymentPath,
    ResourceIntAttrRODeploymentPath,
    ResourceListAttrRODeploymentPath,
    VCenterDeploymentAppAttributeNames,
    VCenterVMFromCloneDeployAppAttributeNames,
    VCenterVMFromImageDeploymentAppAttributeNames,
    VCenterVMFromTemplateDeploymentAppAttributeNames,
    VCenterVMFromVMDeploymentAppAttributeNames,
)


class BaseVCenterDeployApp(DeployApp):
    ATTR_NAMES = VCenterDeploymentAppAttributeNames

    vm_cluster = ResourceAttrRODeploymentPath(ATTR_NAMES.vm_cluster)
    vm_storage = ResourceAttrRODeploymentPath(ATTR_NAMES.vm_storage)
    vm_resource_pool = ResourceAttrRODeploymentPath(ATTR_NAMES.vm_resource_pool)
    vm_location = ResourceAttrRODeploymentPath(ATTR_NAMES.vm_location)
    behavior_during_save = ResourceAttrRODeploymentPath(ATTR_NAMES.behavior_during_save)
    auto_power_on = ResourceBoolAttrRODeploymentPath(ATTR_NAMES.auto_power_on)
    auto_power_off = ResourceBoolAttrRODeploymentPath(ATTR_NAMES.auto_power_off)
    wait_for_ip = ResourceBoolAttrRODeploymentPath(ATTR_NAMES.wait_for_ip)
    auto_delete = ResourceBoolAttrRODeploymentPath(ATTR_NAMES.auto_delete)
    autoload = ResourceBoolAttrRODeploymentPath(ATTR_NAMES.autoload)
    ip_regex = ResourceAttrRODeploymentPath(ATTR_NAMES.ip_regex)
    refresh_ip_timeout = ResourceAttrRODeploymentPath(ATTR_NAMES.refresh_ip_timeout)
    customization_spec = ResourceAttrRODeploymentPath(ATTR_NAMES.customization_spec)
    hostname = ResourceAttrRODeploymentPath(ATTR_NAMES.hostname)
    private_ip = ResourceAttrRODeploymentPath(ATTR_NAMES.private_ip)
    cpu_num = ResourceIntAttrRODeploymentPath(ATTR_NAMES.cpu_num)
    ram_amount = ResourceFloatAttrRODeploymentPath(ATTR_NAMES.ram_amount)
    hdd_specs = HddSpecsAttrRO(ATTR_NAMES.hdd_specs)


class VMFromTemplateDeployApp(BaseVCenterDeployApp):
    ATTR_NAMES = VCenterVMFromTemplateDeploymentAppAttributeNames

    DEPLOYMENT_PATH = constants.VM_FROM_TEMPLATE_DEPLOYMENT_PATH
    vcenter_template = ResourceAttrRODeploymentPath(ATTR_NAMES.vcenter_template)


class VMFromImageDeployApp(BaseVCenterDeployApp):
    ATTR_NAMES = VCenterVMFromImageDeploymentAppAttributeNames

    DEPLOYMENT_PATH = constants.VM_FROM_IMAGE_DEPLOYMENT_PATH
    vcenter_image = ResourceAttrRODeploymentPath(ATTR_NAMES.vcenter_image)
    vcenter_image_arguments = ResourceListAttrRODeploymentPath(
        ATTR_NAMES.vcenter_image_arguments
    )


class VMFromVMDeployApp(BaseVCenterDeployApp):
    ATTR_NAMES = VCenterVMFromVMDeploymentAppAttributeNames

    DEPLOYMENT_PATH = constants.VM_FROM_VM_DEPLOYMENT_PATH
    vcenter_vm = ResourceAttrRODeploymentPath(ATTR_NAMES.vcenter_vm)


class VMFromLinkedCloneDeployApp(VMFromVMDeployApp):
    ATTR_NAMES = VCenterVMFromCloneDeployAppAttributeNames

    DEPLOYMENT_PATH = constants.VM_FROM_LINKED_CLONE_DEPLOYMENT_PATH
    vcenter_vm_snapshot = ResourceAttrRODeploymentPath(ATTR_NAMES.vcenter_vm_snapshot)