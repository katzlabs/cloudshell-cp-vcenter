import sys
from unittest import TestCase

from cloudshell.cp.vcenter.commands.refresh_ip import RefreshIpCommand
from cloudshell.cp.vcenter.common.model_factory import ResourceModelParser
from cloudshell.cp.vcenter.models import GenericDeployedAppResourceModel
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import (
    VMwarevCenterResourceModel,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, create_autospec
else:
    from mock import MagicMock, create_autospec


class TestRefreshIpCommand(TestCase):
    def test_refresh_ip(self):
        nic1 = MagicMock()
        nic1.network = "A Network"
        nic1.ipAddress = ["192.168.1.1"]

        nic2 = MagicMock()
        nic2.network = "A Network"
        nic2.ipAddress = ["111.111.111.111"]

        guest = MagicMock()
        guest.toolsStatus = "toolsOk"
        guest.net = [nic1, nic2]

        vm = MagicMock()
        vm.guest = guest

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        ip_regex = self._create_custom_param("ip_regex", "192\.168\..*")
        refresh_ip_timeout = self._create_custom_param("refresh_ip_timeout", "10")

        resource_model = create_autospec(GenericDeployedAppResourceModel)
        resource_model.fullname = "Generic Deployed App"
        resource_model.vm_uuid = ("123",)
        resource_model.cloud_provider = "vCenter"
        resource_model.vm_custom_params = [ip_regex, refresh_ip_timeout]

        refresh_ip_command = RefreshIpCommand(
            pyvmomi_service, ResourceModelParser(), MagicMock()
        )
        session = MagicMock()
        session.UpdateResourceAddress = MagicMock(return_value=True)
        si = MagicMock()

        center_resource_model = VMwarevCenterResourceModel()
        center_resource_model.default_datacenter = "QualiSB"
        center_resource_model.holding_network = "anetwork"
        cancellation_context = MagicMock()

        # Act
        refresh_ip_command.refresh_ip(
            si=si,
            session=session,
            vcenter_data_model=center_resource_model,
            resource_model=resource_model,
            cancellation_context=cancellation_context,
            logger=MagicMock(),
            app_request_json=MagicMock(),
        )

        # Assert
        self.assertTrue(
            session.UpdateResourceAddress.called_with("machine1", "192.168.1.1")
        )

    def _create_custom_param(self, name, value):
        vm_custom_param = MagicMock()
        vm_custom_param.name = name
        vm_custom_param.value = value
        return vm_custom_param

    def test_refresh_ip_choose_ipv4(self):
        nic1 = MagicMock()
        nic1.network = "A Network"
        nic1.ipAddress = ["192.168.1.1"]

        nic2 = MagicMock()
        nic2.network = "A Network"
        nic2.ipAddress = ["2001:0db8:0a0b:12f0:0000:0000:0000:0001"]

        guest = MagicMock()
        guest.toolsStatus = "toolsOk"
        guest.net = [nic1, nic2]

        vm = MagicMock()
        vm.guest = guest

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        ip_regex = self._create_custom_param("ip_regex", "")
        refresh_ip_timeout = self._create_custom_param("refresh_ip_timeout", "10")

        resource_model = create_autospec(GenericDeployedAppResourceModel)
        resource_model.fullname = "Generic Deployed App"
        resource_model.vm_uuid = ("123",)
        resource_model.cloud_provider = "vCenter"
        resource_model.vm_custom_params = [ip_regex, refresh_ip_timeout]

        refresh_ip_command = RefreshIpCommand(
            pyvmomi_service, ResourceModelParser(), MagicMock()
        )
        session = MagicMock()
        session.UpdateResourceAddress = MagicMock(return_value=True)
        session.GetResourceDetails = MagicMock(return_value=resource_model)
        si = MagicMock()

        center_resource_model = VMwarevCenterResourceModel()
        center_resource_model.default_datacenter = "QualiSB"
        center_resource_model.holding_network = "anetwork"
        cancellation_context = MagicMock()

        # Act
        refresh_ip_command.refresh_ip(
            si=si,
            session=session,
            vcenter_data_model=center_resource_model,
            resource_model=resource_model,
            cancellation_context=cancellation_context,
            logger=MagicMock(),
            app_request_json=MagicMock(),
        )

        # Assert
        self.assertTrue(
            session.UpdateResourceAddress.called_with("machine1", "192.168.1.1")
        )

    def test_refresh_ip_choose_ip_by_regex(self):
        nic1 = MagicMock()
        nic1.network = "A Network"
        nic1.ipAddress = ["192.168.1.1"]

        nic2 = MagicMock()
        nic2.network = "A Network"
        nic2.ipAddress = ["111.111.111.111"]

        guest = MagicMock()
        guest.toolsStatus = "toolsOk"
        guest.net = [nic1, nic2]

        vm = MagicMock()
        vm.guest = guest

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        ip_regex = self._create_custom_param("ip_regex", "192\.168\..*")
        refresh_ip_timeout = self._create_custom_param("refresh_ip_timeout", "10")

        resource_model = create_autospec(GenericDeployedAppResourceModel)
        resource_model.fullname = "Generic Deployed App"
        resource_model.vm_uuid = ("123",)
        resource_model.cloud_provider = "vCenter"
        resource_model.vm_custom_params = [ip_regex, refresh_ip_timeout]

        refresh_ip_command = RefreshIpCommand(
            pyvmomi_service, ResourceModelParser(), MagicMock()
        )
        session = MagicMock()
        session.UpdateResourceAddress = MagicMock(return_value=True)
        session.GetResourceDetails = MagicMock(return_value=resource_model)
        si = MagicMock()

        center_resource_model = VMwarevCenterResourceModel()
        center_resource_model.default_datacenter = "QualiSB"
        center_resource_model.holding_network = "anetwork"
        cancellation_context = MagicMock()

        # Act
        refresh_ip_command.refresh_ip(
            si=si,
            session=session,
            vcenter_data_model=center_resource_model,
            resource_model=resource_model,
            cancellation_context=cancellation_context,
            logger=MagicMock(),
            app_request_json=MagicMock(),
        )

        # Assert
        self.assertTrue(
            session.UpdateResourceAddress.called_with("machine1", "192.168.1.1")
        )

    def test_refresh_ip_should_fail_static_vm(self):
        # Act
        refresh_ip_command = RefreshIpCommand(MagicMock(), MagicMock(), MagicMock())
        # assert
        self.assertRaises(
            ValueError,
            refresh_ip_command.refresh_ip,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            None,
        )
