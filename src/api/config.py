import os

from dotenv import load_dotenv

load_dotenv()

DB_BASE: str = str(os.environ.get("DB_SERVICE_BASE_URL"))


class Routes:
    class Open:
        # PING: str = "/ping"

        class Auth:
            # REGISTER: str = "/auth/register"
            # LOGIN: str = "/auth/login"
            CHECK: str = "/auth"

        # class DB:
        # USERS: str = "/database/users/"
        # GROUPS: str = "/database/groups/"
        # PERMISSIONS: str = "/database/permissions/"
        # RESOURCES: str = "/database/resources/"

        ### USER_GROUPS: str = "/access/view/user-groups"
        ### USER_PERMISSIONS: str = "/access/view/user-permissions"
        ### USER_RESOURCES: str = "/access/view/user-resources"

    class Private:
        USER_IN_GROUP: str = "/access/check/user-in-group"
        PERMISSION_IN_GROUP: str = "/access/check/permission-in-group"
        RESOURCE_IN_PERMISSION: str = "/access/check/resource-in-permission"

        # class User:
        # NAME: str = "/database/users/{user_id}"
        ### GROUPS: str = "/access/view/user-groups"
        ### PERMISSIONS: str = "/access/view/user-permissions"
        ### RESOURCES: str = "/access/view/user-resources"

        # class Group:
        # NAME: str = "/database/groups/{group_id}"
        # USERS: str = "/access/view/group-users"
        # PERMISSIONS: str = "/access/view/group-permissions"
        # RESOURCES: str = "/access/view/group-resources"

        # class Permission:
        # NAME: str = "/database/permissions/{permission_id}"
        # GROUPS: str = "/access/view/permission-groups"
        # USERS: str = "/access/view/permission-users"
        # RESOURCES: str = "/access/view/permission-resources"

        # class Resource:
        # NAME: str = "/database/resources/{resource_id}"
        # USERS: str = "/access/view/resource-users"
        # GROUPS: str = "/access/view/resource-groups"
        # PERMISSIONS: str = "/access/view/resource-permissions"
