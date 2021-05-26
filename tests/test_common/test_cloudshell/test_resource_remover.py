import sys
from unittest import TestCase

from cloudshell.cp.vcenter.common.cloud_shell.resource_remover import (
    CloudshellResourceRemover,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestResourceRemover(TestCase):
    def test_resource_remover(self):
        # assert
        session = MagicMock()
        to_remove = "remove this"

        session.DeleteResource = MagicMock(return_value=True)
        session = MagicMock(return_value=session)
        resource_remmover = CloudshellResourceRemover()

        # act
        resource_remmover.remove_resource(session, to_remove)

        # assert
        self.assertTrue(session.DeleteResource.called_with(to_remove))
