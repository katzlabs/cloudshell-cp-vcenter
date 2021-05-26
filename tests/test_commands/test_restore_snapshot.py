import sys
from unittest import TestCase

from cloudshell.cp.vcenter.commands.restore_snapshot import SnapshotRestoreCommand
from cloudshell.cp.vcenter.exceptions.snapshot_not_found import (
    SnapshotNotFoundException,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, patch
else:
    from mock import MagicMock, patch


class TestSnapshotRestoreCommand(TestCase):
    @patch(
        "cloudshell.cp.vcenter.commands.restore_snapshot.SnapshotRetriever.get_vm_snapshots"
    )
    def test_restore_snapshot_should_success_on_existing_snapshot(
        self, mock_get_vm_snapshots
    ):
        vm = MagicMock()

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        snapshot_restore_command = SnapshotRestoreCommand(
            pyvmomi_service=pyvmomi_service, task_waiter=MagicMock()
        )
        si = MagicMock()

        snapshot = MagicMock()
        mock_get_vm_snapshots.return_value = {"snap1": snapshot}
        session = MagicMock()

        # Act
        snapshot_restore_command.restore_snapshot(
            si=si,
            logger=MagicMock(),
            session=session,
            vm_uuid="machine1",
            resource_fullname="vm_machine1",
            snapshot_name="snap1",
        )

        # Assert
        self.assertTrue(snapshot.RevertToSnapshot_Task.called)

    @patch(
        "cloudshell.cp.vcenter.commands.restore_snapshot.SnapshotRetriever.get_vm_snapshots"
    )
    def test_restore_snapshot_should_throw_exception_on_none_existing_snapshot(
        self, mock_get_vm_snapshots
    ):
        vm = MagicMock()

        pyvmomi_service = MagicMock()
        pyvmomi_service.find_by_uuid = MagicMock(return_value=vm)

        snapshot_restore_command = SnapshotRestoreCommand(
            pyvmomi_service=pyvmomi_service, task_waiter=MagicMock()
        )
        si = MagicMock()

        mock_get_vm_snapshots.return_value = {"snap1": MagicMock()}

        session = MagicMock()

        # Act + Assert
        self.assertRaises(
            SnapshotNotFoundException,
            snapshot_restore_command.restore_snapshot,
            si,
            MagicMock(),
            session,
            "machine1",
            "vm_machine1",
            "NOT_EXISTING_SNAPSHOT",
        )
