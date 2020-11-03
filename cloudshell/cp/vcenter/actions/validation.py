from __future__ import annotations

from collections.abc import Iterable
from logging import Logger

from cloudshell.cp.vcenter.api.client import VCenterAPIClient
from cloudshell.cp.vcenter.exceptions import InvalidAttributeException
from cloudshell.cp.vcenter.resource_config import VCenterResourceConfig

SHUTDOWN_METHODS = ("hard", "soft")
BEHAVIOURS_DURING_SAVE = ("Remain Powered On", "Power Off")


class ValidationActions:
    def __init__(
        self,
        vcenter_client: VCenterAPIClient,
        resource_conf: VCenterResourceConfig,
        logger: Logger,
    ):
        self._vcenter_client = vcenter_client
        self._resource_conf = resource_conf
        self._logger = logger

    def validate_resource_conf(self):
        conf = self._resource_conf
        _is_not_empty(conf.address, "address")
        _is_not_empty(conf.user, conf.ATTR_NAMES.user)
        _is_not_empty(conf.password, conf.ATTR_NAMES.password)
        _is_not_empty(conf.default_datacenter, conf.ATTR_NAMES.default_datacenter)
        _is_not_empty(conf.vm_location, conf.ATTR_NAMES.vm_location)
        _is_value_in(
            conf.shutdown_method, SHUTDOWN_METHODS, conf.ATTR_NAMES.shutdown_method
        )
        _is_value_in(
            conf.behavior_during_save,
            BEHAVIOURS_DURING_SAVE,
            conf.ATTR_NAMES.behavior_during_save,
        )

    def validate_connection(self):
        _ = self._vcenter_client._si  # try to connect

    def validate_dc_objects(self):
        dc = self._vcenter_client.get_dc(self._resource_conf.default_datacenter)
        self._vcenter_client.get_folder(self._resource_conf.vm_location, dc.vmFolder)
        self._vcenter_client.get_network(self._resource_conf.holding_network, dc)
        self._vcenter_client.get_cluster(self._resource_conf.vm_cluster, dc)
        self._vcenter_client.get_storage(self._resource_conf.vm_storage, dc)
        if self._resource_conf.saved_sandbox_storage:
            self._vcenter_client.get_storage(
                self._resource_conf.saved_sandbox_storage, dc
            )
        if self._resource_conf.default_dv_switch:
            self._vcenter_client.get_dv_switch(
                self._resource_conf.default_dv_switch, dc
            )

    def validate_deploy_app(self, deploy_app):
        conf = self._resource_conf
        _one_is_not_empty(
            [deploy_app.vm_cluster, self._resource_conf.vm_cluster],
            conf.ATTR_NAMES.vm_cluster,
        )
        _one_is_not_empty(
            [deploy_app.vm_storage, self._resource_conf.vm_storage],
            conf.ATTR_NAMES.vm_storage,
        )
        _one_is_not_empty(
            [deploy_app.vm_location, self._resource_conf.vm_location],
            conf.ATTR_NAMES.vm_location,
        )


def _is_not_empty(value: str, attr_name: str):
    if not value:
        raise InvalidAttributeException(f"{attr_name} cannot be empty")


def _is_value_in(value: str, expected_values: Iterable[str], attr_name: str):
    if value not in expected_values:
        raise InvalidAttributeException(
            f"{attr_name} should be one of the {list(expected_values)}"
        )


def _one_is_not_empty(values: list, attr_name: str):
    if not any(values):
        raise InvalidAttributeException(f"{attr_name} cannot be empty")
