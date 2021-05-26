import sys
import unittest

from pyVmomi import vim

from cloudshell.cp.vcenter.common.vcenter.task_waiter import SynchronousTaskWaiter

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock, patch
else:
    from mock import MagicMock, patch


task = MagicMock(spec=vim.Task)


class helper:
    @staticmethod
    def change_to_success(a):
        task.info.state = vim.TaskInfo.State.success
        return

    @staticmethod
    def change_to_error(a):
        task.info.state = vim.TaskInfo.State.error
        return


class TestTaskWaiter(unittest.TestCase):
    @patch("time.sleep", helper.change_to_success)
    def test_wait_for_task(self):
        task.info = MagicMock(spec=vim.TaskInfo)
        task.info.state = vim.TaskInfo.State.running
        result = "result"
        task.info.result = result

        waiter = SynchronousTaskWaiter()
        res = waiter.wait_for_task(
            task=task, logger=MagicMock(), action_name="job", hide_result=False
        )

        self.assertEqual(res, result)

    @patch("time.sleep", helper.change_to_success)
    def test_wait_for_queued_task(self):
        task.info = MagicMock(spec=vim.TaskInfo)
        task.info.state = vim.TaskInfo.State.queued
        result = "result"
        task.info.result = result

        waiter = SynchronousTaskWaiter()
        res = waiter.wait_for_task(
            task=task, logger=MagicMock(), action_name="job", hide_result=False
        )

        self.assertEqual(res, result)

    @patch("time.sleep", helper.change_to_success)
    def test_wait_for_task_result_none(self):
        task.info = MagicMock(spec=vim.TaskInfo)
        task.info.state = vim.TaskInfo.State.running
        result = "result"
        task.info.result = None

        waiter = SynchronousTaskWaiter()
        res = waiter.wait_for_task(
            task=task, logger=MagicMock(), action_name="job", hide_result=False
        )

        self.assertIsNone(res, result)

    @patch("time.sleep", helper.change_to_error)
    def test_wait_for_task_fail(self):
        task.info = MagicMock(spec=vim.TaskInfo)
        task.info.error = "error"
        task.info.state = vim.TaskInfo.State.running
        result = "result"
        task.info.result = result

        waiter = SynchronousTaskWaiter()

        self.assertRaises(Exception, waiter.wait_for_task, task)
