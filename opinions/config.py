from dataclasses import dataclass
import os

from ecological import config as eco_config

from . import constants


@dataclass
class FileMountSecrets:
    something_secret: str


secret_keys = ("opinions-something-secret",)


def get_secrets_from_file(secret_dir) -> FileMountSecrets:
    dataset = {}
    for key in secret_keys:
        secret_name = key.replace(
            "opinions-", "").replace("-", "_")
        try:
            with open(os.path.join(secret_dir, key), "r") as fl:
                dataset[secret_name] = fl.read().strip()
        except FileNotFoundError:
            dataset[secret_name] = None

    return FileMountSecrets(**dataset)


class Config(eco_config.Config, prefix="opinions"):
    is_debug: bool = False
    version: str = "0.0.1"
    environment: str = "dev"
    app_name: str = "opinions"

    # redis connection
    redis_host: str = "localhost"
    redis_port: str = "6379"
    redis_db: str = "0"

    # secrets should go in secrets_dir
    secrets_dir: str = ""
    redis_passwd: str = ""
    something_secret: str = ""

    # Defaults for setting later
    REDIS_CONN_STR: str = ""

    def __init__(self):
        if self.secrets_dir is not None:
            # If there are secrets we need to look up
            self.set_secrets()
        self.REDIS_CONN_STR = f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        if self.redis_passwd:
            self.REDIS_CONN_STR = (f"redis://:{self.redis_passwd}@"
                                   f"{self.redis_host}:{self.redis_port}/{self.redis_db}")

        if self.environment == constants.LOCAL:
            self.is_debug = True

    @classmethod
    def set_secrets(cls):
        """Set secrets from files in `secrets_dir`"""
        fm_secrets = get_secrets_from_file(cls.secrets_dir)
        for attrname in filter(lambda it: not it.startswith("__"), dir(fm_secrets)):
            attr_value = getattr(fm_secrets, attrname)
            if attr_value is None:
                raise AttributeError(
                    f"Configuration error: {attrname} is not set.")
            setattr(cls, attrname, attr_value)
