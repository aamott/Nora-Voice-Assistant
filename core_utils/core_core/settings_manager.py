#############################
# Settings Manager
#############################
import yaml
from yaml.loader import SafeLoader


class SettingsManager:

    def __init__(self, settings_file=None):
        if settings_file is None:
            settings_file = "settings.yaml"

        # Load the settings
        with open(settings_file) as file:
            self.settings = yaml.load(file, Loader=SafeLoader)


    # TODO: make this thread safe
    def save_settings(self, settings_file=None) -> bool:
        """ Saves the settings to the settings file"""
        if settings_file is None:
            settings_file = "settings.yaml"

        # Save the settings
        with open(settings_file, 'w') as file:
            yaml.dump(self.settings, file)

        # TODO: return True if the settings were saved, False otherwise
        return True


    def get_setting(self, keys):
        """ Gets the value of the setting using a path
            Parameters:
                keys (string): path to the setting, separated by "."
                                    For example, "speech.stt.google.credentials"
            
            Returns: dict or single value 
        """
        def get_value(keys, settings):
            if "." in keys:
                key, rest = keys.split(".", 1)
                if key not in settings:
                    return None
                return get_value(rest, settings[key])
            else:
                if keys not in settings:
                    return None
                return settings[keys]

        return get_value(keys, self.settings)


    def set_setting(self, setting_path, value):
        """ Sets the value of the setting using a path
            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"
                value (any): value to set 
        """
        def set_value(keys, value, settings):
            if "." in keys:
                key, rest = keys.split(".", 1)
                if key not in settings:
                    settings[key] = {}
                set_value(rest, value, settings[key])
            else:
                if keys not in settings:
                    settings[keys] = {}
                # If value is none, delete the setting
                # if value is None:
                #     del settings[keys]
                # else:
                settings[keys] = value

        set_value(setting_path, value, self.settings)

        # save the settings
        self.save_settings()


    def setting_exists(self, setting_path):
        """ Checks if the setting exists
            Parameters:
                setting_path (string): path to the setting, separated by "."
                                                For example, "speech.stt.google.credentials"

            Returns:
                bool: True if the setting exists, False otherwise
        """
        setting = self.get_setting(setting_path)
        return setting is not None



if __name__ == "__main__":
    settings_manager = SettingsManager()
    settings_manager.__init__()
    # Get a nonexistant setting
    print("Test:", settings_manager.get_setting("test"))
    
    # Set a setting
    settings_manager.set_setting("test", "Success")
    print("Test:", settings_manager.get_setting("test"))

    # Delete the setting
    settings_manager.set_setting("test", None)
    print("Test:", settings_manager.get_setting("test"))

    # Save the settings
    # settings_manager.save_settings()