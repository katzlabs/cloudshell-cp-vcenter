import sys
import unittest

from cloudshell.cp.vcenter.commands.deploy_vm import DeployCommand
from cloudshell.cp.vcenter.models.DeployFromTemplateDetails import (
    DeployFromTemplateDetails,
)
from cloudshell.cp.vcenter.models.vCenterVMFromTemplateResourceModel import (
    vCenterVMFromTemplateResourceModel,
)

if sys.version_info >= (3, 0):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestDeployFromTemplateCommand(unittest.TestCase):
    def test_deploy_execute(self):
        # arrange
        deployer = MagicMock()
        si = MagicMock()
        template_model = MagicMock()

        deploy_res = dict()
        deploy_res["vm_path"] = "path"
        deploy_res["vm_name"] = "name"
        deploy_res["uuid"] = "uuid"

        template_model.template_name = "temp name"
        template_model.vm_folder = "temp folder"
        deployer.deploy_from_template = MagicMock(return_value=deploy_res)

        template_resource_model = vCenterVMFromTemplateResourceModel()

        deploy_params = DeployFromTemplateDetails(
            template_resource_model, "VM Deployment"
        )

        deploy_command = DeployCommand(deployer)

        resource_context = MagicMock()
        logger = MagicMock()
        session = MagicMock()
        app_resource_model = MagicMock()
        vcenter_data_model = MagicMock()
        vcenter_data_model.default_datacenter = "QualiSB"
        vcenter_data_model.vm_location = "TargetFolder"
        reservation_id = "4228128c-fb7e-9b0e-60b8-c3fabd3c624e"
        cancellation_context = object()

        # act
        result = deploy_command.execute_deploy_from_template(
            si=si,
            logger=logger,
            session=session,
            deployment_params=deploy_params,
            app_resource_model=app_resource_model,
            vcenter_data_model=vcenter_data_model,
            reservation_id=reservation_id,
            cancellation_context=cancellation_context,
            folder_manager=MagicMock(),
        )

        # assert
        self.assertTrue(result)
        deployer.deploy_from_template.assert_called_once_with(
            si,
            logger,
            session,
            deploy_params,
            app_resource_model,
            vcenter_data_model,
            reservation_id,
            cancellation_context,
        )

    def test_deploy_image_execute(self):
        deployer = MagicMock()
        si = MagicMock()
        deployment_params = MagicMock()
        deployment_params.template_resource_model.vm_location = "SomeFolder"

        connectivity = MagicMock()
        res = MagicMock()
        deployer.deploy_from_image = MagicMock(return_value=res)
        session = MagicMock()
        vcenter_data_model = MagicMock()
        vcenter_data_model.default_datacenter = "QualiSB"
        logger = MagicMock()
        reservation_id = "4228128c-fb7e-9b0e-60b8-c3fabd3c624e"

        deploy_command = DeployCommand(deployer)
        cancellation_context = object()

        # act
        folder_manager = MagicMock()
        result = deploy_command.execute_deploy_from_image(
            si=si,
            logger=logger,
            session=session,
            vcenter_data_model=vcenter_data_model,
            deployment_params=deployment_params,
            resource_context=connectivity,
            reservation_id=reservation_id,
            cancellation_context=cancellation_context,
            folder_manager=folder_manager,
        )

        # assert
        self.assertTrue(result)
        deployer.deploy_from_image.assert_called_once_with(
            si=si,
            logger=logger,
            session=session,
            vcenter_data_model=vcenter_data_model,
            data_holder=deployment_params,
            resource_context=connectivity,
            reservation_id=reservation_id,
            cancellation_context=cancellation_context,
        )

    def test_deploy_clone_execute(self):
        # arrange
        deployer = MagicMock()
        si = MagicMock()
        template_model = MagicMock()

        deploy_res = dict()
        deploy_res["vm_path"] = "path"
        deploy_res["vm_name"] = "name"
        deploy_res["uuid"] = "uuid"

        template_model.template_name = "temp name"
        template_model.vm_folder = "temp folder"
        deployer.deploy_from_template = MagicMock(return_value=deploy_res)

        reservation_id = "4228128c-fb7e-9b0e-60b8-c3fabd3c624e"
        logger = MagicMock()
        session = MagicMock()
        app_resource_model = MagicMock()

        vcenter_data_model = MagicMock()
        vcenter_data_model.default_datacenter = "QualiSB"
        vcenter_data_model.vm_location = "TargetFolder"

        template_resource_model = vCenterVMFromTemplateResourceModel()

        deploy_params = DeployFromTemplateDetails(
            template_resource_model, "VM Deployment"
        )

        deploy_command = DeployCommand(deployer)

        resource_context = MagicMock()
        cancellation_context = object()

        # act
        result = deploy_command.execute_deploy_clone_from_vm(
            si=si,
            logger=logger,
            session=session,
            vcenter_data_model=vcenter_data_model,
            app_resource_model=app_resource_model,
            deployment_params=deploy_params,
            reservation_id=reservation_id,
            cancellation_context=cancellation_context,
            folder_manager=MagicMock(),
        )

        # assert
        self.assertTrue(result)
        deployer.deploy_clone_from_vm.assert_called_once_with(
            si,
            logger,
            session,
            deploy_params,
            app_resource_model,
            vcenter_data_model,
            reservation_id,
            cancellation_context,
        )

    def test_deploy_snapshot_execute(self):
        # arrange
        deployer = MagicMock()
        si = MagicMock()
        template_model = MagicMock()

        deploy_res = dict()
        deploy_res["vm_path"] = "path"
        deploy_res["vm_name"] = "name"
        deploy_res["uuid"] = "uuid"

        template_model.template_name = "temp name"
        template_model.vm_folder = "temp folder"
        deployer.deploy_from_template = MagicMock(return_value=deploy_res)

        template_resource_model = vCenterVMFromTemplateResourceModel()

        deploy_params = DeployFromTemplateDetails(
            template_resource_model, "VM Deployment"
        )

        deploy_command = DeployCommand(deployer)

        resource_context = MagicMock()
        logger = MagicMock()
        vcenter_data_model = MagicMock()
        vcenter_data_model.default_datacenter = "QualiSB"
        vcenter_data_model.vm_location = "TargetFolder"
        reservation_id = "4228128c-fb7e-9b0e-60b8-c3fabd3c624e"
        cancellation_context = object()
        session = MagicMock()
        app_resource_model = MagicMock()

        # act
        result = deploy_command.execute_deploy_from_linked_clone(
            si=si,
            logger=logger,
            session=session,
            deployment_params=deploy_params,
            vcenter_data_model=vcenter_data_model,
            app_resource_model=app_resource_model,
            reservation_id=reservation_id,
            cancellation_context=cancellation_context,
            folder_manager=MagicMock(),
        )

        # assert
        self.assertTrue(result)
        deployer.deploy_from_linked_clone.assert_called_once_with(
            si,
            logger,
            session,
            deploy_params,
            app_resource_model,
            vcenter_data_model,
            reservation_id,
            cancellation_context,
        )
