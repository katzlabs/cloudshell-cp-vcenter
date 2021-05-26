import sys
import unittest

from cloudshell.cp.vcenter.common.model_factory import ResourceModelParser
from cloudshell.cp.vcenter.common.vcenter.data_model_retriever import (
    VCenterDataModelRetriever,
)
from cloudshell.cp.vcenter.models.QualiDriverModels import ResourceContextDetails

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, create_autospec
else:
    from mock import MagicMock, create_autospec


class TestVCenterDataModelRetriever(unittest.TestCase):
    def test_get_vcenter_data_model(self):
        # Arrange
        data_model_retriever = VCenterDataModelRetriever(ResourceModelParser())
        api = MagicMock()
        vcenter_resource = create_autospec(ResourceContextDetails)

        vcenter_resource.model = "VMWare vCenter"
        vcenter_resource.attrib = {
            "user": "uzer",
            "password": "pwd",
            "default_dvswitch": "",
            "holding_network": "",
            "vm_cluster": "",
            "vm_resource_pool": "",
            "vm_storage": "",
            "vm_location": "",
            "shutdown_method": "",
            "ovf_tool_path": "",
            "execution_server_selector": "",
            "reserved_networks": "",
            "default_datacenter": "",
            "promiscuous_mode": "",
            "behavior_during_save": "",
            "saved_sandbox_storage": "",
        }

        api.GetResourceDetails = MagicMock(return_value=vcenter_resource)

        # Act
        vcenter_data_model = data_model_retriever.get_vcenter_data_model(
            api, "VMWare Center"
        )

        # Assert
        self.assertEqual(vcenter_data_model.user, "uzer")

    def test_get_vcenter_data_model_empty_vcenter_name(self):
        # Arrange
        data_model_retriever = VCenterDataModelRetriever(ResourceModelParser())
        api = MagicMock()
        vcenter_resource = create_autospec(ResourceContextDetails)

        vcenter_resource.model = "VMWare vCenter"
        vcenter_resource.attrib = {
            "user": "uzer",
            "password": "pwd",
            "default_dvswitch": "",
            "holding_network": "",
            "vm_cluster": "",
            "vm_resource_pool": "",
            "vm_storage": "",
            "vm_location": "",
            "shutdown_method": "",
            "ovf_tool_path": "",
            "execution_server_selector": "",
            "reserved_networks": "",
            "default_datacenter": "",
            "promiscuous_mode": "",
        }

        api.GetResourceDetails = MagicMock(return_value=vcenter_resource)

        # Act + Assert
        self.assertRaises(
            ValueError, data_model_retriever.get_vcenter_data_model, api, ""
        )
