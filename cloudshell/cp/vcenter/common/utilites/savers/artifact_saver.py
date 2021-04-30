from cloudshell.cp.vcenter.common.utilites.savers.linked_clone_artifact_saver import (
    LinkedCloneArtifactHandler,
)


class ArtifactHandler(object):
    @staticmethod
    def factory(
        saveDeploymentModel,
        pv_service,
        vcenter_data_model,
        si,
        logger,
        session,
        app_resource_model,
        deployer,
        reservation_id,
        resource_model_parser,
        snapshot_saver,
        task_waiter,
        folder_manager,
        port_configurer,
        cancellation_service,
    ):
        return LinkedCloneArtifactHandler(
            pv_service,
            vcenter_data_model,
            si,
            logger,
            session,
            app_resource_model,
            deployer,
            reservation_id,
            resource_model_parser,
            snapshot_saver,
            task_waiter,
            folder_manager,
            port_configurer,
            cancellation_service,
        )
