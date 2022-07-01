################################
# Web Server
# https://fastapi.tiangolo.com/tutorial/first-steps/
# Starting and stopping the server:
#       https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
################################
from socket import create_server
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import contextlib
import time
import threading
import uvicorn

from .core_core.channels import Channels
from .core_core.settings_manager import SettingsManager

# get routers
from .server_resources.routers import auth, settings

###########################
# Server class
# Manages a threaded instance of Uvicorn. 
###########################
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


def create_app(channels: Channels,
               settings_manager: SettingsManager) -> FastAPI:
    """Create the configured FastAPI app instance"""
    app = FastAPI()

    # include routes
    app.include_router(auth.router)
    app.include_router(settings.router, prefix="/settings")
    settings.settings_manager = settings_manager

    channels = channels
    settings_manager = settings_manager



    @app.get("/")
    async def root():
        # redirect to the home page
        return RedirectResponse(url="/index.htm")


    # Create endpoints for all the html files
    app.mount("/", StaticFiles(directory="core_utils/server_resources/pages"), name="site", )

    return app




def create_server(channels: Channels,
                    settings_manager: SettingsManager):
    """ Creates an instance of the server
    """
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
    channels = Channels()
    settings_manager = SettingsManager(settings_file="settings.yaml")
    # Launch the server
    server = create_server(channels=channels, settings_manager=settings_manager)

    with server.run_in_thread():
        while True:
            time.sleep(1)
            # code can be run in here while the server is going