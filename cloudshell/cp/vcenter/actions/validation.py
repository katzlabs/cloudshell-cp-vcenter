class ValidationActions:
    def __init__(self, vcenter_client, logger):
        """Init command.

        :param cloudshell.cp.azure.api.client.VCenterAPIClient vcenter_client:
        :param logging.Logger logger:
        """
        self._vcenter_client = vcenter_client
        self._logger = logger
