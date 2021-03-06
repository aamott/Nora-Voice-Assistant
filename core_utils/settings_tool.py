#########################
# Settings Tool
# Wrapper for the settings manager
# Passed into skills to allow them to access settings.
##########################
from core_utils.core_core.settings_manager import SettingsManager


class SettingsTool:

    def __init__(self, settings_manager : SettingsManager, setting_path: str='') -> None:
        """ Initializes the settings tool

        Args:
            settings_manager (SettingsManager): The settings manager
            setting_path (str): The path to the setting subsection (ex. speech.stt.google). 
                                        Changes to settings will only be made in this subsection.
        """
        self.settings_manager = settings_manager
        self.setting_path = setting_path


    def get_setting(self, keys, default=None) -> object:
        """ Gets the value of the setting using a path. If the setting does not exist and
            the default value is set, the setting is created and default returned.
            If the default value is not set, None is returned.

            Parameters:
                keys (string): path to the setting, separated by "."
                                    For example, "speech.stt.google.credentials"
            
            Returns: any: the value of the setting, or None if the setting does not exist
        """
        return self.settings_manager.get_setting(self.setting_path + "." + keys, default=default)


    def set_setting(self, setting_path, value):
        """ Sets the value of the setting using a path. Creates the setting if it doesn't exist.

            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"
                value (any): value to set
        """
        self.settings_manager.set_setting(self.setting_path + "." + setting_path, value)


    def create_setting(self, setting_path, default_value=None):
        """ Adds a setting to the settings manager without overwriting an existing value.
        
            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"
                default_value (any): value to set if the setting does not exist
        """
        # settings_manager handles the creation of the setting
        self.settings_manager.create_setting(self.setting_path + "." + setting_path, default_value)


    def save_settings(self) -> bool:
        """ Saves the settings to disk

            Returns:
                bool: True if the settings were saved, False otherwise 
        """
        return self.settings_manager.save_settings()


    def setting_exists(self, setting_path) -> bool:
        """ Checks if the setting exists

            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"
            Returns:
                bool: True if the setting exists, False otherwise
        """
        return self.settings_manager.setting_exists(self.setting_path + "." + setting_path)


    def get_sub_tool(self, setting_path: str):
        """ Gets a sub tool for a setting path
        
            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"
            Returns:
                SettingsTool: The sub tool
        """
        return SettingsTool(self.settings_manager, self.setting_path + "." + setting_path)



if __name__ == "__main__":

    # Setup
    settings_manager = SettingsManager()
    settings_manager.__init__()
    settings_tool = SettingsTool(settings_manager, "speech.stt.google")
    # Test
    print(settings_tool.get_setting("credentials"))
    settings_tool.set_setting("credentials", "test credentials")
    print(settings_tool.get_setting("credentials"))