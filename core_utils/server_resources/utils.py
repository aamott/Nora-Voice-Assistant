"""utils.py
This code was modified from
https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/
"""
# Should be a full path to the config file relative to the parent directory
CONFIG_PATH = "core_utils/server_resources/.config"

import os
from configparser import ConfigParser
from secrets import token_bytes
from base64 import b64encode

def get_env_config():
    """Sets up configuration for the app
    
    """

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(CONFIG_PATH)

        try:
            config = config["OAUTH"]
        except KeyError:
            # create a new config file and fill it with the default values
            config = ConfigParser()
            NEW_SECRET_KEY = b64encode(token_bytes(32)).decode()
            config["OAUTH"] = {
                "SECRET_KEY": NEW_SECRET_KEY,
                "ALGORITHM": "HS256",
                "ACCESS_TOKEN_EXPIRE_MINUTES": 30
            }
            with open(CONFIG_PATH, "w") as file:
                config.write(file)

            raise KeyError("No configuration found in " + CONFIG_PATH)

    else:
        print("Warning! Using a generated key. It will be gone by the end of the sess")
        config = {
            "SECRET_KEY":
            os.getenv("SECRET_KEY", None ),
            "ALGORITHM":
            os.getenv("ALGORITHM", "HS256"),
            "ACCESS_TOKEN_EXPIRE_MINUTES":
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        }
        if not config["SECRET_KEY"]:
            print("No secret key set. Generating a new key.\n")
            config["SECRET_KEY"] = b64encode(token_bytes(32)).decode()

    return config
