import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.vcenter.common.utilites.common_name import generate_unique_name
from cloudshell.cp.vcenter.vm.dvswitch_connector import VirtualSwitchToMachineConnector
from cloudshell.cp.vcenter.vm.portgroup_configurer import *
from cloudshell.cp.vcenter.vm.vnic_to_network_mapper import VnicToNetworkMapper

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, create_autospec, patch
else:
    from mock import MagicMock, create_autospec, patch


class TestVirtualSwitchToMachineConnector(TestCase):
    def setUp(self):
        self._si = None
        self.virtual_machine_path = "SergiiT"
        self.virtual_machine_name = "JustTestNeedToBeRemoved"
        self.vm_uuid = "422254d5-5226-946e-26fb-60c21898b731"

        self.vcenter_name = "QualiSB"
        self.dv_switch_path = "QualiSB"
        self.network_path = "QualiSB"

        self.dv_switch_name = "dvSwitch-SergiiT"
        self.dv_port_group_name = "aa-dvPortGroup3B"

        self.network = MagicMock()
        self.network.key = "network-key"
        self.network.config.distributedVirtualSwitch.uuid = (
            "422254d5-5226-946e-26fb-60c21898b73f"
        )
        self.py_vmomi_service = MagicMock()

        self.vm = MagicMock()
        self.vm.config.hardware = MagicMock()
        self.vnic = MagicMock(spec=vim.vm.device.VirtualEthernetCard)
        self.vnic.deviceInfo = MagicMock()
        self.vm.config.hardware.device = [self.vnic]

        self.py_vmomi_service.find_by_uuid = lambda a, b, c: self.vm
        self.py_vmomi_service.find_network_by_name = MagicMock(
            return_value=self.network
        )

        self.synchronous_task_waiter = MagicMock()
        self.synchronous_task_waiter.wait_for_task = MagicMock(return_value="TASK OK")
        self.si = MagicMock()

        name_generator = generate_unique_name
        vnic_to_network_mapper = VnicToNetworkMapper(name_generator)
        helpers = MagicMock()
        cs_retriever_service = MagicMock()
        session = MagicMock()
        resource_context = MagicMock()
        connection_details = MagicMock()

        helpers.get_resource_context_details = MagicMock(return_value=resource_context)
        helpers.get_api_session = MagicMock(return_value=session)
        cs_retriever_service.getVCenterConnectionDetails = MagicMock(
            return_value=connection_details
        )

        self.configurer = VirtualMachinePortGroupConfigurer(
            self.py_vmomi_service,
            self.synchronous_task_waiter,
            vnic_to_network_mapper,
            MagicMock(),
            MagicMock(),
        )

        # pyvmomi_service, synchronous_task_waiter, vnic_to_network_mapper, vnic_common

        self.creator = DvPortGroupCreator(
            self.py_vmomi_service, self.synchronous_task_waiter
        )
        self.connector = VirtualSwitchToMachineConnector(self.creator, self.configurer)

    def test_map_vnc(self):
        network_spec = MagicMock()
        network_spec.dv_port_name = ""
        network_spec.dv_switch_name = ""
        network_spec.dv_switch_path = ""
        network_spec.vlan_id = ""
        network_spec.vlan_spec = ""
        mapp = [network_spec]

        self.configurer.connect_vnic_to_networks = MagicMock(return_value="OK")
        self.connector.virtual_machine_port_group_configurer.connect_by_mapping = (
            MagicMock(return_value="OK")
        )
        self.connector.connect_and_get_vm = MagicMock(
            return_value=(
                1,
                1,
            )
        )

        res = self.connector.connect_by_mapping(
            self.si, self.vm, [], "default_network", [], MagicMock(), "True"
        )
        self.assertEqual(res, "OK")
        res = self.connector.connect_by_mapping(
            self.si, self.vm, [], None, [], MagicMock(), "True"
        )
        self.assertEqual(res, "OK")

        res = self.connector.connect_by_mapping(
            self.si, self.vm, mapp, "default_network", [], MagicMock(), "True"
        )
        self.assertEqual(res, "OK")
        res = self.connector.connect_by_mapping(
            self.si, self.vm, mapp, None, [], MagicMock(), "True"
        )
        self.assertEqual(res, "OK")
