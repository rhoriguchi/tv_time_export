import sys
import json
import logging
import yaml
from datetime import datetime
from pathlib import Path

from tv_time_export.request_handler import RequestHandler

logger = logging.getLogger(__name__)


class TvTimeExtractor(object):
    def __init__(self):
        self._content = self._read_config()

    def get_all_tv_show_states(self):
        results = {}

        for user in self._content["users"]:
            username = user["username"]
            password = user["password"]

            logger.info(f"Logging in as {username}")

            request_handler = RequestHandler(username, password)
            request_handler.login()

            results[username] = request_handler.get_all_tv_show_states()

        return results

    def save_tv_show_states(self, all_tv_show_states):
        save_path = self._content["save_path"]

        if not save_path.is_dir():
            raise ValueError(f'save_path "{save_path}" does not exist')

        datetime_string = (
            datetime.now()
            .isoformat("T", "seconds")
            .replace("-", "")
            .replace(":", "")
        )

        for username, tv_show_states in all_tv_show_states.items():
            file_name = f"{username}_{datetime_string}.json"
            file_path = save_path / file_name

            logger.info(f'Saving data to "{file_path}"')

            with open(file_path, "w") as file:
                json.dump(tv_show_states, file, separators=(",", ":"))

    @staticmethod
    def _get_config_path():
        argv = sys.argv

        if len(argv) >= 2:
            config_path = Path(argv[1])

            if config_path.is_absolute():
                return config_path
            else:
                return Path.cwd() / config_path
        else:
            return Path.cwd() / "config.yaml"

    def _read_config(self):
        config_path = self._get_config_path()

        if not config_path.exists():
            raise ValueError(f'Config path "{config_path}" does not exist')

        logger.info(f'Reading "{config_path}"')

        with open(config_path, "r") as stream:
            content = yaml.safe_load(stream)

        if "users" not in content or not content["users"]:
            raise ValueError("users list is empty in config.yaml")

        for i, user in enumerate(content["users"]):
            if not user.get("username"):
                raise ValueError(f"username is empty for users[{i}]")

            if not user.get("password"):
                raise ValueError(f"password is empty for users[{i}]")

        if "save_path" not in content or content["save_path"] is None:
            content["save_path"] = Path.cwd()

        content["save_path"] = Path(content["save_path"])

        if not content["save_path"].exists():
            raise ValueError(
                f'Config path "{content["save_path"]}" does not exist'
            )

        log_content = {
            "users": [
                {
                    "username": user["username"],
                    "password": "*****",
                }
                for user in content["users"]
            ],
            "save_path": str(content["save_path"]),
        }

        logger.info(f"Config values: {log_content}")

        return content
