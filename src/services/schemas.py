from pydantic import BaseModel, PositiveInt


class BaseRequest(BaseModel):
    request_id: str
    error: bool


class AccessPermissionRequest(BaseRequest):
    request_type: str = "access_permission"
    user_id: str
    permission_id: PositiveInt
    permission_groups: list[str]
    user_groups: list[str]


class JoinGroupRequest(BaseRequest):
    request_type: str = "join_group"
    user_id: str
    group_id: PositiveInt
    user_groups: list[str]
    user_permissions: list[str]


class RemovePermissionRequest(BaseRequest):
    request_type: str = "remove_permission"
    user_id: str
    permission_id: PositiveInt


class ExcludeFromGroupRequest(BaseRequest):
    request_type: str = "exclude_from_group"
    user_id: str
    group_id: PositiveInt


class ViewUserGroups(BaseRequest):
    request_type: str = "view_user_groups"
    user_groups: list[str] = [
        "",
    ]
    user_id: str
    pass


class GetResourcePermissionRequest(BaseRequest):
    request_type: str = "get_resource_permission"
    user_id: str
    resource_id: PositiveInt
    resource_permissions: list[str] = [
        "",
    ]
    pass
