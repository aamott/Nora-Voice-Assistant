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

    channels = channels
    settings_manager = settings_manager

    @app.get("/")
    async def root():
        # redirect to index.htm
        return RedirectResponse(url="/index.htm")


    @app.get("/settings")
    async def get_settings():
        return settings_manager.get_settings()

    
    @app.get("/settings/{setting_path}")
    async def get_setting(setting_path: str):
        return settings_manager.get_setting(setting_path)


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



if __name__ == "__main__":
    channels = channels.Channels()
    settings_manager = settings_manager.SettingsManager(settings_file="settings.yaml")
    # Launch the server
    server = create_server(channels=channels, settings_manager=settings_manager)

    with server.run_in_thread():
        while True:
            time.sleep(1)
            # code can be run in here while the server is going