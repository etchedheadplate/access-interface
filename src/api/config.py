import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DB_BASE = str(os.environ.get("DB_SERVICE_BASE_URL"))


@dataclass
class DBRoutes:
    SERVICE_PING = "/ping"

    AUTH_REGISTER = "/auth/register"
    AUTH_LOGIN = "/auth/login"
    AUTH_CHECK = "/authenticated-route"
