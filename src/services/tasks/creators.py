import secrets
import string
from typing import Any, cast
from uuid import UUID

from pydantic import PositiveInt

from src.services.clients import GroupClient, PermissionClient, UserClient
from src.services.tasks.schemas import (
    AccessPermissionTask,
    ExcludeFromGroupTask,
    GetResourcePermissionTask,
    JoinGroupTask,
    RemovePermissionTask,
    ViewUserGroupsTask,
)


class TaskCreator:
    def __init__(self, request_type: str, user_id: UUID):
        self.request_id = self._generate_id()
        self.request_type = request_type
        self.user_id = user_id
        self.error = False
        self.result: str | list[str] = ""

    def _generate_id(self, length: int = 8) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    async def create(
        self, **args: Any
    ) -> (
        AccessPermissionTask
        | ExcludeFromGroupTask
        | GetResourcePermissionTask
        | JoinGroupTask
        | RemovePermissionTask
        | ViewUserGroupsTask
    ):
        constructed_task = await self._construct(**args)
        return constructed_task

    async def _construct(
        self, **args: Any
    ) -> (
        AccessPermissionTask
        | ExcludeFromGroupTask
        | GetResourcePermissionTask
        | JoinGroupTask
        | RemovePermissionTask
        | ViewUserGroupsTask
    ):
        raise NotImplementedError


class AccessPermissionCreator(TaskCreator):
    async def _construct(self, **args: Any) -> AccessPermissionTask:
        permission_id: PositiveInt = cast(PositiveInt, args["permission_id"])

        try:
            async with PermissionClient() as permission_client:
                get_permission_groups = await permission_client.get_groups(permission_id=permission_id)
            permission_groups = [group["name"] for group in get_permission_groups]  # type: ignore[index]

            async with UserClient() as user_client:
                get_user_groups = await user_client.get_groups(user_id=self.user_id)
            user_groups = [group["name"] for group in get_user_groups]  # type: ignore[index]

        except Exception:
            self.error = True
            permission_groups = []
            user_groups = []

        return AccessPermissionTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            permission_id=permission_id,
            permission_groups=permission_groups,
            user_groups=user_groups,
            error=self.error,
        )


class JoinGroupCreator(TaskCreator):
    async def _construct(self, **args: Any) -> JoinGroupTask:
        group_id: PositiveInt = cast(PositiveInt, args["group_id"])

        try:
            async with GroupClient() as group_client:
                get_group_name = await group_client.get(group_id=group_id)
            group_name = get_group_name["name"]

            async with UserClient() as user_client:
                get_user_groups = await user_client.get_groups(user_id=self.user_id)
                get_user_permissions = await user_client.get_permissions(user_id=self.user_id)
            user_groups = [group["name"] for group in get_user_groups]  # type: ignore[index]
            user_permissions = [permission["name"] for permission in get_user_permissions]  # type: ignore[index]

        except Exception:
            self.error = True
            group_name = ""
            user_groups = []
            user_permissions = []

        return JoinGroupTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            group_id=group_id,
            group_name=group_name,
            user_groups=user_groups,
            user_permissions=user_permissions,
            error=self.error,
        )


class RemovePermissionCreator(TaskCreator):
    async def _construct(self, **args: Any) -> RemovePermissionTask:
        permission_id: PositiveInt = cast(PositiveInt, args["permission_id"])

        return RemovePermissionTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            permission_id=permission_id,
            error=self.error,
        )


class ExcludeFromGroupCreator(TaskCreator):
    async def _construct(self, **args: Any) -> ExcludeFromGroupTask:
        group_id: PositiveInt = cast(PositiveInt, args["group_id"])

        try:
            async with GroupClient() as group_client:
                get_group_name = await group_client.get(group_id=group_id)
            group_name = get_group_name["name"]

            async with UserClient() as user_client:
                get_user_groups = await user_client.get_groups(user_id=self.user_id)
            user_groups = [group["name"] for group in get_user_groups]  # type: ignore[index]

        except Exception:
            self.error = True
            group_name = ""
            user_groups = []

        return ExcludeFromGroupTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            group_id=group_id,
            group_name=group_name,
            user_groups=user_groups,
            error=self.error,
        )


class ViewUserGroupsCreator(TaskCreator):
    async def _construct(self, **args: Any) -> ViewUserGroupsTask:

        return ViewUserGroupsTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            error=self.error,
        )


class GetResourcePermissionCreator(TaskCreator):
    async def _construct(self, **args: Any) -> GetResourcePermissionTask:
        resource_id: PositiveInt = cast(PositiveInt, args["resource_id"])

        return GetResourcePermissionTask(
            request_id=self.request_id,
            user_id=str(self.user_id),
            resource_id=resource_id,
            error=self.error,
        )


def get_task_creator(request_type: str, user_id: UUID) -> TaskCreator:
    creator = CreatorMapping.TASK[request_type]
    return creator(request_type, user_id)


class CreatorMapping:
    TASK = {
        "access_permission": AccessPermissionCreator,
        "join_group": JoinGroupCreator,
        "remove_permission": RemovePermissionCreator,
        "exclude_from_group": ExcludeFromGroupCreator,
        "view_user_groups": ViewUserGroupsCreator,
        "get_resource_permission": GetResourcePermissionCreator,
    }
