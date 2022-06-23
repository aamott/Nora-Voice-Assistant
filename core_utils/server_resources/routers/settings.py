from typing import Union
from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from core_core.settings_manager import SettingsManager

router = APIRouter()

settings_manager = SettingsManager("settings.yaml")

class Setting(BaseModel):
    value: Union[int, float, bool, list, str]


@router.get("/settings")
async def get_settings():
    return settings_manager.get_settings()


@router.get("/settings/{setting_path}")
async def get_setting(setting_path: str = Query(
        title="Get setting",
        description="Get a setting by dot-separated path")):
    return settings_manager.get_setting(setting_path)


# # TODO: Test endpoint
@router.put("/settings/{setting_path}")
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


@router.post("/settings/{setting_path}")
async def post_setting(
        setting_path: str,
        setting_value: Setting):
    # setting_value = value.value
    # print("Setting: " + setting_path + " = " + setting_value)
    settings_manager.set_setting(setting_path, setting_value.value)