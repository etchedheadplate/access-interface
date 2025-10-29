from uuid import UUID

from pydantic import BaseModel, PositiveInt


class BaseRequest(BaseModel):
    request_id: str


class AccessPermissionRequest(BaseRequest):
    request_type: str = "access_permission"
    user_id: UUID
    permission_id: PositiveInt
    permission_groups: list[str]
    user_groups: list[str]


class JoinGroupRequest(BaseRequest):
    request_type: str = "join_group"
    user_id: UUID
    group_id: PositiveInt
    user_groups: list[str]
    user_permissions: list[str]


class RemovePermissionRequest(BaseRequest):
    request_type: str = "remove_permission"
    user_id: UUID
    permission_id: PositiveInt


class ExcludeFromGroupRequest(BaseRequest):
    request_type: str = "exclude_from_group"
    user_id: UUID
    group_id: PositiveInt


class ViewUserGroups(BaseRequest):
    request_type: str = "view_user_groups"
    user_id: UUID
    pass


class GetResourcePermissionRequest(BaseRequest):
    request_type: str = "get_resource_permission"
    user_id: UUID
    resource_id: PositiveInt
    pass
