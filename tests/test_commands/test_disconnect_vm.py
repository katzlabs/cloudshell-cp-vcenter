import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.vcenter.commands.disconnect_dvswitch import (
    VirtualSwitchToMachineDisconnectCommand,
)
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import (
    VMwarevCenterResourceModel,
)
from cloudshell.cp.vcenter.network.vnic.vnic_service import VNicService

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestVirtualSwitchToMachineDisconnectCommand(TestCase):
    def test_delete_all(self):
        # arrange
        uuid = "uuid"
        si = MagicMock()
        vm = MagicMock()

        connection_detail = MagicMock()
        connection_detail.host = MagicMock()
        connection_detail.username = MagicMock()
        connection_detail.password = MagicMock()
        connection_detail.port = MagicMock()

        pv_service = MagicMock()
        pv_service.connect = MagicMock(return_value=si)
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        connector = VirtualSwitchToMachineDisconnectCommand(
            pv_service, MagicMock(), "anetwork"
        )
        connector.get_network_by_name = lambda x, y: MagicMock()

        vcenter_data_model = VMwarevCenterResourceModel()

        # act
        res = connector.disconnect(
            si=si,
            logger=MagicMock(),
            vcenter_data_model=vcenter_data_model,
            vm_uuid=uuid,
            network_name=None,
            vm=None,
        )
        # assert
        self.assertTrue(
            pv_service.connect.called_with(
                connection_detail.host,
                connection_detail.username,
                connection_detail.password,
                connection_detail.port,
            )
        )
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        # self.assertTrue(virtual_switch_to_machine_connector.remove_interfaces_from_vm.called_with(vm))
        self.assertTrue(res)

    def test_delete(self):
        # arrange
        uuid = "uuid"
        network_name = "network_name"

        network = MagicMock()
        network.name = network_name
        si = MagicMock()
        vm = MagicMock()
        vm.network = [network]

        connection_detail = MagicMock()
        connection_detail.host = MagicMock()
        connection_detail.username = MagicMock()
        connection_detail.password = MagicMock()
        connection_detail.port = MagicMock()

        pv_service = MagicMock()
        pv_service.connect = MagicMock(return_value=si)
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        connector = VirtualSwitchToMachineDisconnectCommand(
            pv_service, MagicMock(), "anetwork"
        )

        vcenter_data_model = VMwarevCenterResourceModel()

        # act
        res = connector.disconnect(
            si=si,
            logger=MagicMock(),
            vcenter_data_model=vcenter_data_model,
            vm_uuid=uuid,
            network_name=network_name,
        )

        # assert
        self.assertTrue(
            pv_service.connect.called_with(
                connection_detail.host,
                connection_detail.username,
                connection_detail.password,
                connection_detail.port,
            )
        )
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(res)

    def test_is_device_match_network_port_type(self):
        # arrange
        backing = MagicMock(spec=[])
        device = MagicMock()
        port = MagicMock()

        device.backing = backing
        backing.port = port
        port.portgroupKey = "port key"

        # act
        res = VNicService.device_is_attached_to_network(device, port.portgroupKey)

        # assert
        self.assertTrue(res)

    def test_is_device_match_network_other_type(self):
        # arrange
        backing = MagicMock(spec=[])
        device = MagicMock()
        nerwork = MagicMock()

        device.backing = backing
        backing.network = nerwork
        nerwork.name = "vln name or network name"

        # act
        res = VNicService.device_is_attached_to_network(device, nerwork.name)

        # assert
        self.assertTrue(res)

    def test_is_device_match_network_not_found(self):
        # arrange
        device = MagicMock()
        device.backing = MagicMock(spec=[])

        virtual_switch_to_machine_connector = VirtualSwitchToMachineDisconnectCommand(
            MagicMock(), MagicMock(), "anetwork"
        )

        # act
        res = VNicService.device_is_attached_to_network(device, "Fake name")

        # assert
        self.assertFalse(res)

    def test_remove_interfaces_from_vm_no_nic_found(self):
        # arrange
        vm = MagicMock()
        vm.config = MagicMock()
        vm.config.hardware()
        vm.config.hardware.device = []

        virtual_switch_to_machine_connector = VirtualSwitchToMachineDisconnectCommand(
            MagicMock(), MagicMock(), "anetwork"
        )

        # act
        res = virtual_switch_to_machine_connector.remove_interfaces_from_vm_task(vm)

        # assert
        self.assertIsNone(res)

    def test_remove_interfaces_from_vm_no_filter(self):
        # arrange
        device1 = MagicMock(spec=vim.vm.device.VirtualEthernetCard)
        device2 = MagicMock(spec=vim.vm.device.VirtualSoundCard)
        vm = MagicMock()
        vm.config = MagicMock()
        vm.config.hardware()
        vm.config.hardware.device = [device2, device1]

        virtual_switch_to_machine_connector = VirtualSwitchToMachineDisconnectCommand(
            MagicMock(), MagicMock(), "anetwork"
        )

        # act
        res = virtual_switch_to_machine_connector.remove_interfaces_from_vm_task(vm)

        # assert
        self.assertTrue(res)

    def test_remove_interfaces_from_vm_with_filter(self):
        # arrange
        device1 = MagicMock(spec=vim.vm.device.VirtualEthernetCard)
        device2 = MagicMock(spec=vim.vm.device.VirtualEthernetCard)
        device3 = MagicMock(spec=vim.vm.device.VirtualSoundCard)

        device1.name = "this is the one"
        device2.name = "very close"
        device3.name = "not it"

        vm = MagicMock()
        vm.config = MagicMock()
        vm.config.hardware()
        vm.config.hardware.device = [device3, device2, device1]

        connector = VirtualSwitchToMachineDisconnectCommand(
            MagicMock(), MagicMock(), "anetwork"
        )

        # act
        condition = lambda device: device.name == device1.name
        res = connector.remove_interfaces_from_vm_task(vm, condition)

        # assert
        self.assertTrue(res)
