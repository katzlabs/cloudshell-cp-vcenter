import sys
from unittest import TestCase

from cloudshell.cp.vcenter.commands.retrieve_snapshots import RetrieveSnapshotsCommand

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, patch
else:
    from mock import MagicMock, patch


class TestRetrieveSnapshotCommand(TestCase):
    @patch(
        "cloudshell.cp.vcenter.commands.restore_snapshot.SnapshotRetriever.get_vm_snapshots"
    )
    def test_restore_snapshot_should_success_on_existing_snapshot(
        self, mock_get_vm_snapshots
    ):
        vm = MagicMock()

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        snapshot_restore_command = RetrieveSnapshotsCommand(
            pyvmomi_service=pyvmomi_service
        )
        si = MagicMock()

        mock_get_vm_snapshots.return_value = {"snap1": MagicMock()}

        # Act
        snapshots = snapshot_restore_command.get_snapshots(
            si=si, logger=MagicMock(), vm_uuid="machine1"
        )

        # Assert
        self.assertSequenceEqual(snapshots, ["snap1"])
