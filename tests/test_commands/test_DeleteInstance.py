import sys
import unittest

from pyVmomi import vim

from cloudshell.cp.vcenter.commands.DeleteInstance import DestroyVirtualMachineCommand

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, create_autospec
else:
    from mock import MagicMock, create_autospec


class TestDestroyVirtualMachineCommand(unittest.TestCase):
    def test_destroyVirtualMachineCommand(self):
        # arrange
        pv_service = MagicMock()
        folder_manager = MagicMock()
        resource_remover = MagicMock()
        disconnector = MagicMock()
        si = create_autospec(spec=vim.ServiceInstance)
        resource_name = "this/is the name of the template"
        uuid = "uuid"
        vm = MagicMock()

        pv_service.destory_vm = MagicMock(return_value=True)
        disconnector.remove_interfaces_from_vm = MagicMock(return_value=True)
        resource_remover.remove_resource = MagicMock(return_value=True)
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        reservation_details = MagicMock()
        reservation_details.ReservationDescription = MagicMock()
        reservation_details.ReservationDescription.Connectors = []

        session = MagicMock()
        session.GetReservationDetails = MagicMock(return_value=reservation_details)
        vcenter_data_model = MagicMock()
        destroyer = DestroyVirtualMachineCommand(
            pv_service, folder_manager, resource_remover, disconnector
        )

        # act
        res = destroyer.destroy(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=vcenter_data_model,
            vm_uuid=uuid,
            vm_name=resource_name,
            reservation_id="reservation_id",
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(pv_service.destory_vm.called_with(vm))
        self.assertTrue(disconnector.remove_interfaces_from_vm.called_with(si, vm))
        self.assertTrue(resource_remover.remove_resource.called_with(resource_name))
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))

    def test_destroyVirtualMachineCommandDeletesResourceWhenTheVMActualllyRemovedInVCenter(
        self,
    ):
        # arrange
        pv_service = MagicMock()
        folder_manager = MagicMock()
        resource_remover = MagicMock()
        disconnector = MagicMock()
        si = create_autospec(spec=vim.ServiceInstance)
        resource_name = "this/is the name of the template"
        uuid = "uuid"
        vm = None

        pv_service.destory_vm = MagicMock(return_value=True)
        disconnector.remove_interfaces_from_vm = MagicMock(return_value=True)
        resource_remover.remove_resource = MagicMock(return_value=True)
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        reservation_details = MagicMock()
        reservation_details.ReservationDescription = MagicMock()
        reservation_details.ReservationDescription.Connectors = []

        session = MagicMock()
        session.GetReservationDetails = MagicMock(return_value=reservation_details)
        vcenter_data_model = MagicMock()
        destroyer = DestroyVirtualMachineCommand(
            pv_service, folder_manager, resource_remover, disconnector
        )

        # act
        res = destroyer.destroy(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=vcenter_data_model,
            vm_uuid=uuid,
            vm_name=resource_name,
            reservation_id="reservation_id",
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(pv_service.destory_vm.called_with(vm))
        self.assertTrue(disconnector.remove_interfaces_from_vm.called_with(si, vm))
        self.assertTrue(resource_remover.remove_resource.called_with(resource_name))
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))

    def test_destroyVirtualMachineOnlyCommand(self):
        # arrange
        pv_service = MagicMock()
        folder_manager = MagicMock()
        resource_remover = MagicMock()
        disconnector = MagicMock()
        si = create_autospec(spec=vim.ServiceInstance)
        vm = MagicMock()

        resource_model = MagicMock()
        resource_model.vm_uuid = "uuid"
        resource_model.fullname = "this/is the name of the template"
        resource_model.app_request_model.vm_location = "vm folder"
        reservation_id = "9e5b7004-e62e-4a8d-be1a-96bd1e58cb13"

        pv_service.destory_mv = MagicMock(return_value=True)
        disconnector.remove_interfaces_from_vm = MagicMock(return_value=True)
        resource_remover.remove_resource = MagicMock(return_value=True)
        pv_service.find_by_uuid = MagicMock(return_value=vm)

        reservation_details = MagicMock()
        reservation_details.ReservationDescription = MagicMock()
        reservation_details.ReservationDescription.Connectors = []

        session = MagicMock()
        session.GetReservationDetails = MagicMock(return_value=reservation_details)
        vcenter_data_model = MagicMock()
        vcenter_data_model.default_datacenter = "Default Datacenter"

        destroyer = DestroyVirtualMachineCommand(
            pv_service, folder_manager, resource_remover, disconnector
        )

        # act
        res = destroyer.DeleteInstance(
            si=si,
            logger=MagicMock(),
            session=session,
            vcenter_data_model=vcenter_data_model,
            reservation_id=reservation_id,
            resource_model=resource_model,
        )

        # assert
        self.assertTrue(res)
        self.assertTrue(pv_service.destory_mv.called_with(vm))
        self.assertTrue(disconnector.remove_interfaces_from_vm.called_with(si, vm))
        self.assertTrue(pv_service.find_by_uuid.called_with(si, resource_model.vm_uuid))
