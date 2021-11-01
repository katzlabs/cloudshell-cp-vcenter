from pyVmomi import vim


def is_vnic(device) -> bool:
    return isinstance(device, vim.vm.device.VirtualEthernetCard)


def is_virtual_disk(device) -> bool:
    return isinstance(device, vim.vm.device.VirtualDisk)


def is_virtual_scsi_controller(device) -> bool:
    return isinstance(device, vim.vm.device.VirtualSCSIController)


def get_device_key(device):
    return device.key


def get_all_devices(vm):
    return vm.config.hardware.device


def get_vnics(vm) -> list:
    return list(filter(is_vnic, get_all_devices(vm)))


def get_virtual_disks(vm) -> list:
    return list(filter(is_virtual_disk, get_all_devices(vm)))