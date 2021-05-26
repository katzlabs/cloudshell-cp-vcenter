import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.vcenter.commands.power_manager_vm import (
    VirtualMachinePowerManagementCommand,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestVirtualMachinePowerManagementCommand(TestCase):
    def test_power_off_already(self):
        vm_uuid = "uuid"
        si = MagicMock(spec=vim.ServiceInstance)
        vm = MagicMock(spec=vim.VirtualMachine)
        vm.summary = MagicMock()
        vm.summary.runtime = MagicMock()
        vm.summary.runtime.powerState = "poweredOff"
        session = MagicMock()
        pv_service = MagicMock()
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        power_manager = VirtualMachinePowerManagementCommand(
            pv_service, MagicMock(), MagicMock()
        )

        # act
        res = power_manager.power_off(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=MagicMock(),
            vm_uuid=vm_uuid,
            resource_fullname=None,
        )

        # assert
        self.assertTrue(res, "Already powered off")
        self.assertFalse(vm.PowerOn.called)

    def test_power_on_already(self):
        vm_uuid = "uuid"
        si = MagicMock(spec=vim.ServiceInstance)
        vm = MagicMock(spec=vim.VirtualMachine)
        vm.summary = MagicMock()
        vm.summary.runtime = MagicMock()
        vm.summary.runtime.powerState = "poweredOn"
        session = MagicMock()
        pv_service = MagicMock()
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        power_manager = VirtualMachinePowerManagementCommand(
            pv_service, MagicMock(), MagicMock()
        )

        # act
        res = power_manager.power_on(
            si=si,
            logger=MagicMock(),
            session=session,
            vm_uuid=vm_uuid,
            resource_fullname=None,
        )

        # assert
        self.assertTrue(res, "Already powered on")
        self.assertFalse(vm.PowerOn.called)

    def test_power_on(self):
        # arrange
        vm_uuid = "uuid"
        si = MagicMock(spec=vim.ServiceInstance)
        vm = MagicMock(spec=vim.VirtualMachine)
        session = MagicMock()
        pv_service = MagicMock()
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        task = MagicMock()

        vm.PowerOn = MagicMock(return_value=task)

        synchronous_task_waiter = MagicMock()
        synchronous_task_waiter.wait_for_task = MagicMock(return_value=True)

        power_manager = VirtualMachinePowerManagementCommand(
            pv_service, synchronous_task_waiter, MagicMock()
        )

        # act
        res = power_manager.power_on(
            si=si,
            logger=MagicMock(),
            session=session,
            vm_uuid=vm_uuid,
            resource_fullname=None,
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(synchronous_task_waiter.wait_for_task.called_with(task))
        self.assertTrue(vm.PowerOn.called)

    def test_power_off_soft(self):
        # arrange
        vcenter_name = "vcenter name"
        vm_uuid = "uuid"
        session = MagicMock()
        si = MagicMock(spec=vim.ServiceInstance)
        vm = MagicMock(spec=vim.VirtualMachine)
        task = MagicMock()
        pv_service = MagicMock()
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        vm.PowerOff = MagicMock(return_value=task)

        synchronous_task_waiter = MagicMock()
        synchronous_task_waiter.wait_for_task = MagicMock(return_value=True)

        power_manager = VirtualMachinePowerManagementCommand(
            pv_service, synchronous_task_waiter, MagicMock()
        )
        power_manager._connect_to_vcenter = MagicMock(return_value=si)
        power_manager._get_vm = MagicMock(return_value=vm)

        vcenter = MagicMock()
        vcenter.shutdown_method = "soft"
        # act
        res = power_manager.power_off(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=vcenter,
            vm_uuid=vm_uuid,
            resource_fullname=None,
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(vm.ShutdownGuest.called)
        self.assertTrue(power_manager._connect_to_vcenter.called_with(vcenter_name))
        self.assertTrue(power_manager._get_vm.called_with(si, vm_uuid))
        self.assertTrue(synchronous_task_waiter.wait_for_task.called_with(task))

    def test_power_off_hard(self):
        # arrange
        vcenter_name = "vcenter name"
        vm_uuid = "uuid"
        session = MagicMock()
        si = MagicMock(spec=vim.ServiceInstance)
        vm = MagicMock(spec=vim.VirtualMachine)
        task = MagicMock()
        pv_service = MagicMock()
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        vm.PowerOff = MagicMock(return_value=task)

        synchronous_task_waiter = MagicMock()
        synchronous_task_waiter.wait_for_task = MagicMock(return_value=True)

        power_manager = VirtualMachinePowerManagementCommand(
            pv_service, synchronous_task_waiter, MagicMock()
        )
        power_manager._connect_to_vcenter = MagicMock(return_value=si)
        power_manager._get_vm = MagicMock(return_value=vm)

        vcenter = MagicMock()
        vcenter.shutdown_method = "hard"
        # act
        res = power_manager.power_off(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=vcenter,
            vm_uuid=vm_uuid,
            resource_fullname=None,
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(vm.PowerOff.called)
        self.assertTrue(power_manager._connect_to_vcenter.called_with(vcenter_name))
        self.assertTrue(power_manager._get_vm.called_with(si, vm_uuid))
        self.assertTrue(synchronous_task_waiter.wait_for_task.called_with(task))
