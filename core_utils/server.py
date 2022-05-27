################################
# Web Server
# https://fastapi.tiangolo.com/tutorial/first-steps/
# Starting and stopping the server:
#       https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
################################
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core_core import channels, settings_manager


class Server(FastAPI):
    def __init__(self, channels: channels.Channels, settings_manager: settings_manager.SettingsManager):

        self.channels = channels
        self.settings_manager = settings_manager

        super().__init__(title="Core", description="Core Server")
        self.mount("/", StaticFiles(directory="server"), name="site")

        # self.app.add_event_handler("startup", self.startup)
        # self.app.add_event_handler("shutdown", self.shutdown)



        @self.get("/")
        async def root():
            return {"message": "Hello World"}


        @self.get("/settings")
        async def read_user_me():
            return {"settings": "some settings"}


# Launch the server
server = Server(channels.Channels(), settings_manager.SettingsManager())
# server.app.run(host="
app=server