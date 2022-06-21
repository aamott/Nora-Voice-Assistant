################################
# Web Server
# https://fastapi.tiangolo.com/tutorial/first-steps/
# Starting and stopping the server:
#       https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
################################
from typing import Union
from socket import create_server
from fastapi import FastAPI, Query, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import contextlib
import time
import threading
from pydantic import BaseModel
import uvicorn

from core_core import channels, settings_manager


class Server(uvicorn.Server):

    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def create_app(channels: channels.Channels,
               settings_manager: settings_manager.SettingsManager) -> FastAPI:
    app = FastAPI()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    channels = channels
    settings_manager = settings_manager

    class Setting(BaseModel):
        # name: str
        value: Union[int, float, bool, list, str]

    @app.get("/")
    async def root():
        # redirect to the home page
        return RedirectResponse(url="/index.htm")


    @app.get("/settings")
    async def get_settings():
        return settings_manager.get_settings()


    @app.get("/settings/{setting_path}")
    async def get_setting(setting_path: str = Query(
            title="Get setting",
            description="Get a setting by dot-separated path")):
        return settings_manager.get_setting(setting_path)


    # # TODO: Test endpoint
    @app.put("/settings/{setting_path}")
    async def put_setting(
            setting_path: str,
            value: Setting):
        # TODO: Do we need to filter the value?
        # setting_path = setting_path.replace("/", ".")
        #  check if the setting exists
        if not settings_manager.setting_exists(setting_path):
            # set the setting and return 201 Created
            status_code = status.HTTP_201_CREATED

        return settings_manager.set_setting(setting_path, value.value)


    @app.post("/settings/{setting_path}")
    async def post_setting(
            setting_path: str,
            setting_value: Setting):
        # setting_value = value.value
        # print("Setting: " + setting_path + " = " + setting_value)
        settings_manager.set_setting(setting_path, setting_value.value)


    # Create endpoints for all the html files
    app.mount("/", StaticFiles(directory="core_utils/server"), name="site")

    return app




def create_server(channels: channels.Channels,
                    settings_manager: settings_manager.SettingsManager):
    app = create_app(channels=channels, settings_manager=settings_manager)

    config = uvicorn.Config(app=app,
                            host="127.0.0.1",
                            port=5000,
                            log_level="info")
    server = Server(config=config)

    return server


################################
# Helper Functions
################################
# Function to store the users dictionary in a pickle file.
def store_users(users: dict):
    import pickle
    with open("users.pickle", "wb") as file:
        pickle.dump(users, file)


# Function to load the users dictionary from a pickle file.
def load_users():
    import pickle
    try:
        with open("users.pickle", "rb") as file:
            users = pickle.load(file)
    except FileNotFoundError:
        users = {}
    return users


if __name__ == "__main__":
    channels = channels.Channels()
    settings_manager = settings_manager.SettingsManager(settings_file="settings.yaml")
    # Launch the server
    server = create_server(channels=channels, settings_manager=settings_manager)

    with server.run_in_thread():
        while True:
            time.sleep(1)
            # code can be run in here while the server is going