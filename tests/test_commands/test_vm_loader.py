import sys
from unittest import TestCase

from pyVmomi import vim

from cloudshell.cp.vcenter.commands.load_vm import VMLoader

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestCommandOrchestrator(TestCase):
    def setUp(self):
        self.vc_model = MagicMock()
        self.vc_model.default_datacenter = "datacenter"
        self.pv_service = MagicMock()
        self.vm_loader = VMLoader(self.pv_service)
        self.si = MagicMock()

    def test_get_vm_uuid(self):
        vm = MagicMock(spec=vim.VirtualMachine)
        vm.config = MagicMock()
        vm.config.uuid = "this is the uuid"
        self.pv_service.find_vm_by_name = MagicMock(return_value=vm)
        path = "raz/abadi\\c"
        res = self.vm_loader.load_vm_uuid_by_name(self.si, self.vc_model, path)

        self.assertEqual(res, vm.config.uuid)
        self.assertTrue(
            self.pv_service.find_vm_by_name.called_with(
                self.si, self.vc_model.default_datacenter + "/" + "raz/abadi", "c"
            )
        )

    def test_get_vm_uuid_not_vm(self):
        vm = MagicMock()
        vm.config = MagicMock()
        vm.config.uuid = "this is the uuid"
        self.pv_service.find_vm_by_name = MagicMock(return_value=vm)

        self.assertRaises(
            ValueError,
            self.vm_loader.load_vm_uuid_by_name,
            self.si,
            self.vc_model,
            "path",
        )

    def test_get_vm_uuid_None(self):
        vm = None
        self.pv_service.find_vm_by_name = MagicMock(return_value=vm)

        self.assertRaises(
            ValueError,
            self.vm_loader.load_vm_uuid_by_name,
            self.si,
            self.vc_model,
            "path",
        )
