from cloudshell.shell.standards.core.resource_config_entities import (
    GenericResourceConfig,
    PasswordAttrRO,
    ResourceAttrRO,
    ResourceBoolAttrRO,
    ResourceListAttrRO,
)

from cloudshell.cp.vcenter.constants import SHELL_NAME


class VCenterResourceConfig(GenericResourceConfig):
    user = ResourceAttrRO("User", ResourceAttrRO.NAMESPACE.SHELL_NAME)

    password = PasswordAttrRO("Password", PasswordAttrRO.NAMESPACE.SHELL_NAME)

    default_dv_switch = ResourceAttrRO(
        "Default dvSwitch", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    holding_network = ResourceAttrRO(
        "Holding Network", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    vm_cluster = ResourceAttrRO("VM Cluster", ResourceAttrRO.NAMESPACE.SHELL_NAME)

    vm_resource_pool = ResourceAttrRO(
        "VM Resource Pool", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    vm_storage = ResourceAttrRO("VM Storage", ResourceAttrRO.NAMESPACE.SHELL_NAME)

    saved_sandbox_storage = ResourceAttrRO(
        "Saved Sandbox Storage", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    behavior_during_save = ResourceAttrRO(
        "Behavior during save", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    vm_location = ResourceAttrRO("VM Location", ResourceAttrRO.NAMESPACE.SHELL_NAME)

    shutdown_method = ResourceAttrRO(
        "Shutdown Method", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    ovf_tool_path = ResourceAttrRO("OVF Tool Path", ResourceAttrRO.NAMESPACE.SHELL_NAME)

    reserved_networks = ResourceListAttrRO(
        "Reserved Networks", ResourceListAttrRO.NAMESPACE.SHELL_NAME
    )

    execution_server_selector = ResourceAttrRO(
        "Execution Server Selector", ResourceAttrRO.NAMESPACE.SHELL_NAME
    )

    promiscuous_mode = ResourceBoolAttrRO(
        "Promiscuous Mode", ResourceBoolAttrRO.NAMESPACE.SHELL_NAME
    )

    @classmethod
    def from_context(cls, context, shell_name=SHELL_NAME, api=None, supported_os=None):
        """Creates an instance of a Resource by given context.

        :param str shell_name: Shell Name
        :param list supported_os: list of supported OS
        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        :rtype: GenericResourceConfig
        """
        return super(VCenterResourceConfig, cls).from_context(
            context=context,
            shell_name=shell_name,
            api=api,
            supported_os=supported_os)
