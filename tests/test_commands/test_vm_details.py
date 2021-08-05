import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.core.models import (
    VmDetailsData,
    VmDetailsNetworkInterface,
    VmDetailsProperty,
)

from cloudshell.cp.vcenter.commands.vm_details import VmDetailsCommand
from cloudshell.cp.vcenter.vm.ip_manager import VMIPManager
from cloudshell.cp.vcenter.vm.vm_details_provider import (
    VmDetailsData,
    VmDetailsProvider,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, patch
else:
    from mock import MagicMock, patch


class TestVmDetailsCommand(TestCase):
    @patch(
        "cloudshell.cp.vcenter.network.vnic.vnic_service.VNicService.get_network_by_device"
    )
    def test(self, get_network_by_device):
        # ARRANGE
        network = MagicMock()
        network.name = "Net1"
        network.config.defaultPortConfig.vlan.vlanId = "65"
        get_network_by_device.return_value = network
        vm = self.mock_vm()
        si = MagicMock()
        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)
        ip_regex_param = MagicMock()
        ip_regex_param.name = "ip_regex"
        ip_regex_param.value = ".*"
        wait_for_ip_param = MagicMock()
        wait_for_ip_param.name = "wait_for_ip"
        wait_for_ip_param.value = "True"
        request = MagicMock()
        request.deployedAppJson.name = "App1"
        request.deployedAppJson.vmdetails.vmCustomParams = [
            ip_regex_param,
            wait_for_ip_param,
        ]
        request.appRequestJson.deploymentService.model = "vCenter Clone VM From VM"
        request.appRequestJson.deploymentService.attributes = [MagicMock()]
        resource_context = MagicMock()
        resource_context.attributes = {"Reserved Networks": "Net1;B"}
        cancellation_context = MagicMock(is_cancelled=False)
        ip_manager = VMIPManager()
        vm_details_provider = VmDetailsProvider(pyvmomi_service, ip_manager)
        # ACT
        command = VmDetailsCommand(pyvmomi_service, vm_details_provider)
        datas = command.get_vm_details(
            si=si,
            logger=MagicMock(),
            resource_context=resource_context,
            requests=[request],
            cancellation_context=cancellation_context,
        )
        # ASSERT
        self.assertEqual(len(datas), 1)
        vm_details = datas[0]
        if isinstance(vm_details, VmDetailsData):
            pass
        self.assertEqual(vm_details.appName, "App1")
        self.assertEqual(vm_details.errorMessage, "")
        self.assertEqual(len(vm_details.vmInstanceData), 8)

        self.assertEqual(len(vm_details.vmNetworkData), 1)
        nic = vm_details.vmNetworkData[0]

        if isinstance(nic, VmDetailsNetworkInterface):
            pass

        self.assertEqual(nic.interfaceId, "Mac1")
        self.assertEqual(nic.isPredefined, True)
        self.assertEqual(nic.isPrimary, True)
        self.assertEqual(nic.networkId, "65")

        self.assertEqual(len(nic.networkData), 4)

        self.assertEqual(self._get_value(nic.networkData, "IP"), "1.2.3.4")
        self.assertEqual(self._get_value(nic.networkData, "MAC Address"), "Mac1")
        self.assertEqual(
            self._get_value(nic.networkData, "Network Adapter"), "NetDeviceLabel"
        )
        self.assertEqual(self._get_value(nic.networkData, "Port Group Name"), "Net1")

    def mock_vm(self):
        vm = MagicMock()
        vm.summary.config.memorySizeMB = 2 * 1024
        disk = vim.vm.device.VirtualDisk()
        disk.capacityInKB = 20 * 1024 * 1024
        nic = vim.vm.device.VirtualEthernetCard()
        nic.key = 2
        nic.deviceInfo = vim.Description()
        nic.deviceInfo.label = "NetDeviceLabel"
        nic.macAddress = "Mac1"
        vm.config.hardware.device = [disk, nic]
        vm.summary.config.numCpu = 4
        vm.summary.config.guestFullName = "Centos"
        node = MagicMock()
        node.snapshot = MagicMock()
        node.name = "Snap1"
        vm.snapshot.rootSnapshotList = [
            node
        ]  # [MagicMock(snapshot=snapshot,name=MagicMock(return_value='Snap1'))]
        vm.snapshot.currentSnapshot = node.snapshot
        vm.guest.net = [MagicMock(deviceConfigId="2", ipAddress=["1.2.3.4"])]
        vm.guest.ipAddress = "1.2.3.4"
        return vm

    def _get_value(self, data, key):
        for item in data:
            if item.key == key:
                return item.value
        return None
