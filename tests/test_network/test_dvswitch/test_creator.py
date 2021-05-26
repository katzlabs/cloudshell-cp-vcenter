import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.vcenter.network.dvswitch.creator import DvPortGroupCreator

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, create_autospec
else:
    from mock import MagicMock, create_autospec


class TestDvPortGroupCreator(TestCase):
    def test_create_dv_port_group_exception(self):
        # Arrange
        pyvmomy_service = MagicMock()
        pyvmomy_service.find_network_by_name = MagicMock(return_value=None)
        synchronous_task_waiter = MagicMock()

        # Act
        dv_port_group_creator = DvPortGroupCreator(
            pyvmomy_service, synchronous_task_waiter
        )

        # Assert
        self.assertRaises(
            Exception,
            dv_port_group_creator._create_dv_port_group,
            "port_name",
            "switch_name",
            "switch_path",
            MagicMock(),
            None,
            None,
            MagicMock(),
        )

    def test_create_dv_port_group(self):
        # Arrange
        dv_switch = create_autospec(spec=vim.DistributedVirtualSwitch)
        dv_switch.portgroup = MagicMock()
        pyvmomy_service = MagicMock()
        pyvmomy_service.find_network_by_name = MagicMock(return_value=dv_switch)
        synchronous_task_waiter = MagicMock()
        dv_port_group_creator = DvPortGroupCreator(
            pyvmomy_service, synchronous_task_waiter
        )
        dv_port_group_create_task_prev = DvPortGroupCreator.__dict__[
            "dv_port_group_create_task"
        ]
        DvPortGroupCreator.dv_port_group_create_task = MagicMock()

        # Act
        dv_port_group_creator._create_dv_port_group(
            "port_name",
            "switch_name",
            "switch_path",
            create_autospec(spec=vim.ServiceInstance),
            spec=None,
            vlan_id=1001,
            logger=MagicMock(),
            promiscuous_mode="True",
        )

        # Assert
        self.assertTrue(dv_port_group_creator.dv_port_group_create_task.called)
        setattr(
            DvPortGroupCreator,
            "dv_port_group_create_task",
            dv_port_group_create_task_prev,
        )

    def test_dv_port_group_create_task(self):
        # arrange
        pyvmomy_service = MagicMock()
        synchronous_task_waiter = MagicMock()
        dv_port_group_creator = DvPortGroupCreator(
            pyvmomy_service, synchronous_task_waiter
        )
        dv_switch = create_autospec(spec=vim.DistributedVirtualSwitch)
        dv_switch.AddDVPortgroup_Task = MagicMock()
        spec = create_autospec(spec=vim.dvs.VmwareDistributedVirtualSwitch.VlanSpec)

        # act
        dv_port_group_creator.dv_port_group_create_task(
            dv_port_name="dv_port_name",
            dv_switch=dv_switch,
            spec=spec,
            vlan_id=1001,
            logger=MagicMock(),
            promiscuous_mode="True",
            num_ports=32,
        )

        # assert
        self.assertTrue(dv_switch.AddDVPortgroup_Task.called)
