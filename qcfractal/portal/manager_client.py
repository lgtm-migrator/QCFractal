from typing import Optional, List, Dict, Any

from qcfractal.portal.components.managers import (
    ManagerName,
    ManagerActivationBody,
    ManagerUpdateBody,
    ManagerStatusEnum,
)
from .client import PortalClient


class ManagerClient(PortalClient):
    def __init__(
        self,
        name_data: ManagerName,
        address: str = "api.qcarchive.molssi.org:443",
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify: bool = True,
    ) -> None:
        """Initializes a ManagerClient

        Parameters
        ----------
        address
            The IP and port of the FractalServer instance ("192.168.1.1:8888")
        username
            The username to authenticate with.
        password
            The password to authenticate with.
        verify
            Verifies the SSL connection with a third party server. This may be False if a
            FractalServer was not provided a SSL certificate and defaults back to self-signed
            SSL keys.
        manager_name
            Information about this manager's name
        """

        PortalClient.__init__(
            self, address=address, username=username, password=password, verify=verify, cache=None, max_memcache_size=0
        )

        self.manager_name_data = name_data

    def _update_on_server(self, manager_update: ManagerUpdateBody) -> None:
        return self._auto_request(
            "patch",
            f"v1/manager/{self.manager_name_data.fullname}",
            ManagerUpdateBody,
            None,
            None,
            manager_update,
            None,
        )

    def activate(
        self,
        manager_version: str,
        qcengine_version: str,
        programs: Dict[str, Any],
        tags: List[str],
    ) -> None:
        """Registers/Activates a manager for use on the server

        If an error occurs, an exception is raised.
        """

        manager_info = {
            "name_data": self.manager_name_data,
            "manager_version": manager_version,
            "qcengine_version": qcengine_version,
            "username": self.username,
            "programs": programs,
            "tags": tags,
        }

        return self._auto_request(
            "post",
            "v1/manager",
            ManagerActivationBody,
            None,
            None,
            manager_info,
            None,
        )

    def deactivate(
        self,
        total_worker_walltime: float,
        total_task_walltime: float,
        active_tasks: int,
        active_cores: int,
        active_memory: float,
    ) -> None:
        manager_update = ManagerUpdateBody(
            status=ManagerStatusEnum.inactive,
            total_worker_walltime=total_worker_walltime,
            total_task_walltime=total_task_walltime,
            active_tasks=active_tasks,
            active_cores=active_cores,
            active_memory=active_memory,
        )

        return self._update_on_server(manager_update)

    def heartbeat(
        self,
        total_worker_walltime: float,
        total_task_walltime: float,
        active_tasks: int,
        active_cores: int,
        active_memory: float,
    ) -> None:

        manager_update = ManagerUpdateBody(
            status=ManagerStatusEnum.active,
            total_worker_walltime=total_worker_walltime,
            total_task_walltime=total_task_walltime,
            active_tasks=active_tasks,
            active_cores=active_cores,
            active_memory=active_memory,
        )

        return self._update_on_server(manager_update)
