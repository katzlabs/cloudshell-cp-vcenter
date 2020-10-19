from cloudshell.shell.core.driver_context import AutoLoadDetails


class VCenterAutoloadFlow:
    def __init__(self, resource_config, vcenter_client, logger):
        """Init command.

        :param resource_config:
        :param vcenter_client:
        :param logging.Logger logger:
        """
        self._resource_config = resource_config
        self._vcenter_client = vcenter_client
        self._logger = logger

    def discover(self):
        """Discover command.

        :return:
        """
        return AutoLoadDetails([], [])
