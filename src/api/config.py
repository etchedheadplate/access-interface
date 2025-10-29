import os

from dotenv import load_dotenv

load_dotenv()

DB_BASE = str(os.environ.get("DB_SERVICE_BASE_URL"))


class Routes:
    class Open:
        PING = "/ping"

        class Auth:
            REGISTER = "/auth/register"
            LOGIN = "/auth/login"
            CHECK = "/auth"

        class DB:
            USERS = "/database/users/"
            GROUPS = "/database/groups"
            PERMISSIONS = "/database/permissions"
            RESOURCES = "/database/resources"

    class Private:
        USER_IN_GROUP = "/access/check/user-in-group"
        PERMISSION_IN_GROUP = "/access/check/permission-in-group"
        RESOURCE_IN_PERMISSION = "/access/check/resource-in-permission"

        class User:
            GROUPS = "/access/view/user-groups"
            PERMISSIONS = "/access/view/user-permissions"
            RESOURCES = "/access/view/user-resources"

        class Group:
            USERS = "/access/view/group-users"
            PERMISSIONS = "/access/view/group-permissions"
            RESOURCES = "/access/view/group-resources"

        class Permission:
            ID = "/database/permissions/{permission_id}"
            GROUPS = "/access/view/permission-groups"
            USERS = "/access/view/permission-users"
            RESOURCES = "/access/view/permission-resources"

        class Resource:
            USERS = "/access/view/resource-users"
            GROUPS = "/access/view/resource-groups"
            PERMISSIONS = "/access/view/resource-permissions"
