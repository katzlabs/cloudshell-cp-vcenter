from __future__ import annotations

import itertools
from abc import ABC, abstractmethod

from pyVmomi import vim, vmodl

from cloudshell.cp.vcenter.common.vcenter.data_retrieve_service import (
    VcenterDataRetrieveService,
)
from cloudshell.cp.vcenter.handlers.dc_handler import DcHandler
from cloudshell.cp.vcenter.models.DeployDataHolder import DeployDataHolder


class AbstractAttributeHint(ABC):
    @property
    @staticmethod
    @abstractmethod
    def ATTR_NAME() -> str:
        pass

    def __init__(self, request: DeployDataHolder, dc: DcHandler):
        self._request = request
        self._deployment_path = request.DeploymentPath
        # todo use handlers
        self._si = dc._si._si
        self._datacenter = dc._entity

    def prepare_hints(self) -> dict:
        return {
            "AttributeName": f"{self._deployment_path}.{self.ATTR_NAME}",
            "Values": self._get_hints(),
        }

    @abstractmethod
    def _get_hints(self) -> list[str]:
        pass


class VcenterTemplateAttributeHint(AbstractAttributeHint):
    ATTR_NAME = "vCenter Template"
    ROOT_VMS_FOLDER = "vm"
    SEARCH_VM_TEMPLATES = True

    NAME_PROPERTY = "name"
    PARENT_PROPERTY = "parent"
    IS_TEMPLATE_PROPERTY = "config.template"

    def _generate_full_vm_path(
        self,
        vm_with_props: vmodl.query.PropertyCollector.ObjectContent,
        folders_with_props_map: dict[
            vim.Folder, vmodl.query.PropertyCollector.ObjectContent
        ],
    ) -> str:
        """Generate full path to the VM/Template."""
        service = VcenterDataRetrieveService()
        full_path = service.get_object_property(self.NAME_PROPERTY, vm_with_props)
        parent = service.get_object_property(self.PARENT_PROPERTY, vm_with_props)

        while parent:
            loaded_folder_prop = folders_with_props_map[parent]
            parent_folder_name = service.get_object_property(
                self.NAME_PROPERTY, loaded_folder_prop
            )

            if parent_folder_name == self.ROOT_VMS_FOLDER:
                break

            full_path = f"{parent_folder_name}/{full_path}"

            parent = service.get_object_property(
                self.PARENT_PROPERTY, loaded_folder_prop
            )

        return full_path

    def _get_hints(self) -> list[str]:
        service = VcenterDataRetrieveService()
        hints = []
        # todo: add config.template = True in the filter search. I'm sure it's possible
        vms_with_props = service.get_all_objects_with_properties(
            vim_type=vim.VirtualMachine,
            properties=[
                self.NAME_PROPERTY,
                self.PARENT_PROPERTY,
                self.IS_TEMPLATE_PROPERTY,
            ],
            si=self._si,
            root=self._datacenter,
        )

        folders_with_props = service.get_all_objects_with_properties(
            vim_type=vim.Folder,
            properties=[self.NAME_PROPERTY, self.PARENT_PROPERTY],
            si=self._si,
            root=self._datacenter,
        )

        folders_with_props_map = {prop.obj: prop for prop in folders_with_props}

        for vm_with_props in (
            vm_with_props
            for vm_with_props in vms_with_props
            if self.SEARCH_VM_TEMPLATES
            is service.get_object_property(
                name=self.IS_TEMPLATE_PROPERTY, obj_with_props=vm_with_props
            )
        ):
            hints.append(
                self._generate_full_vm_path(
                    vm_with_props=vm_with_props,
                    folders_with_props_map=folders_with_props_map,
                )
            )

        hints.sort()
        return hints


class VcenterVMAttributeHint(VcenterTemplateAttributeHint):
    ATTR_NAME = "vCenter VM"
    SEARCH_VM_TEMPLATES = False


class VcenterVMSnapshotAttributeHint(VcenterTemplateAttributeHint):
    ATTR_NAME = "vCenter VM Snapshot"
    DEPENDS_ON = VcenterVMAttributeHint.ATTR_NAME

    def _get_hints(self) -> list[str]:
        service = VcenterDataRetrieveService()
        vm_path = next(
            (
                attr.Values[0]
                for attr in self._request.AttributeValues
                if attr.AttributeName.endswith(f".{self.DEPENDS_ON}") and attr.Values
            ),
            None,
        )
        if not vm_path:
            raise Exception(
                f"{self.ATTR_NAME} depends on {self.DEPENDS_ON}. "
                f"Please populate it first."
            )
        vm_obj = service.get_vm_object(self._si, self._datacenter.vmFolder, vm_path)
        return self._get_snapshot_list(vm_obj.snapshot.rootSnapshotList)

    def _get_snapshot_list(self, snapshot_list, response_list=None, snapshot_name=""):
        if not response_list:
            response_list = []
        parent_snapshot_path = snapshot_name
        for snapshot in snapshot_list:
            parent_snapshot_path += snapshot.name
            response_list.append(parent_snapshot_path)
            if snapshot.childSnapshotList:
                parent_snapshot_path += "/"
                self._get_snapshot_list(
                    snapshot.childSnapshotList, response_list, parent_snapshot_path
                )
        return response_list


class VMClusterAttributeHint(AbstractAttributeHint):
    ATTR_NAME = "VM Cluster"
    NAME_PROPERTY = "name"

    def _get_hints(self) -> list[str]:
        service = VcenterDataRetrieveService()
        hints = []

        hosts_with_props = service.get_all_objects_with_properties(
            vim_type=vim.HostSystem,
            properties=[self.NAME_PROPERTY],
            si=self._si,
            root=self._datacenter,
        )

        clusters_with_props = service.get_all_objects_with_properties(
            vim_type=vim.ClusterComputeResource,
            properties=[self.NAME_PROPERTY],
            si=self._si,
            root=self._datacenter,
        )

        for host_with_prop in itertools.chain(hosts_with_props, clusters_with_props):
            hints.append(
                service.get_object_property(
                    name=self.NAME_PROPERTY, obj_with_props=host_with_prop
                )
            )

        hints.sort()
        return hints


class VMStorageAttributeHint(AbstractAttributeHint):
    ATTR_NAME = "VM Storage"
    NAME_PROPERTY = "name"

    def _get_hints(self) -> list[str]:
        service = VcenterDataRetrieveService()
        hints = []

        datastores_with_props = service.get_all_objects_with_properties(
            vim_type=vim.Datastore,
            properties=[self.NAME_PROPERTY],
            si=self._si,
            root=self._datacenter,
        )
        storage_pods_with_props = service.get_all_objects_with_properties(
            vim_type=vim.StoragePod,
            properties=[self.NAME_PROPERTY],
            si=self._si,
            root=self._datacenter,
        )

        for storage_with_prop in itertools.chain(
            datastores_with_props, storage_pods_with_props
        ):
            hints.append(
                service.get_object_property(
                    name=self.NAME_PROPERTY, obj_with_props=storage_with_prop
                )
            )

        hints.sort()
        return hints
