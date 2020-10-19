import ssl

from pyVim.connect import Disconnect, SmartConnect
from pyVmomi import vim


class VCenterAPIClient:
    def __init__(self, host, user, password, logger, port=443):
        """

        :param host:
        :param user:
        :param password:
        :param logger:
        :param port:
        """
        self._logger = logger
        self._si = self._get_si(host=host, user=user, password=password, port=port)

    # todo: check id we need this
    # def back_slash_to_front_converter(string):
    #     """
    #     Replacing all \ in the str to /
    #     :param string: single string to modify
    #     :type string: str
    #     """
    #     pass

    def _get_si_ssl_context_v1(self):
        """

        :return:
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE

        return context

    def _get_si_ssl_context_v2(self):
        """

        :return:
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_NONE

        return context

    def _get_si(self, host, user, password, port):
        """

        :param host:
        :para
        m user:
        :param password:
        :param port:
        :return:
        """
        self._logger.info("Initializing vCenter API client SI...")

        try:
            return SmartConnect(
                host=host,
                user=user,
                pwd=password,
                port=port,
                sslContext=self._get_si_ssl_context_v1(),
            )
        except (ssl.SSLEOFError, vim.fault.HostConnectFault):
            self._logger.exception("TLSv1_2 protocol failed. Trying TLSv1_2 for the vCenter API client SI...")
            return SmartConnect(
                host=host,
                user=user,
                pwd=password,
                port=port,
                sslContext=self._get_si_ssl_context_v2(),
            )
        except vim.fault.InvalidLogin:
            self._logger.exception("Unable to login to the vCenter")
            raise Exception("Can't connect to the vCenter. Invalid user/password")
        except IOError:
            self._logger.exception("Unable to connect to the vCenter")
            raise ValueError("Can't connect to the vCenter. Invalid host address")
