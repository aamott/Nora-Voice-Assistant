#####################
# Setup script

##################
# Set up the user.yaml file:
import os
from passlib.context import CryptContext
import yaml


def create_settings_file():
    filepath = "./settings.yaml"

    # Check if settings.yaml exists:
    overwrite = False
    skip = False
    if os.path.exists(filepath):
        # check if the user wants to overwrite the file:
        while True:
            user_input = input("The settings file already exists. Do you want to skip settings creation, overwrite the file, or append to it?\n([s]kip/[o]verwrite/[A]ppend) ").lower()
            user_input = user_input if user_input else "a"
            if user_input == "o":
                overwrite = True
                break
            elif user_input == "s":
                skip = True
                overwrite = False
                break
            elif user_input == "a":
                overwrite = False
                break

    # If the file does not exist or the user wants to overwrite it:
    if skip:
        print("Skipping settings creation.")
    else:
        print("Please go to the following URL to obtain an access key")
        print("https://console.picovoice.ai/")

        # Gather user input:
        access_key = input("Access Key: ")
        access_key = access_key if access_key else None

        # Create the user dictionary:
        settings = {
            "wakeword": {
                "picovoice": {
                    "key": access_key,
                    "keywords": ['jarvis'],
                    "model_path": None,
                    "sensitivities": None
                }
            }
        }

        if overwrite:
            # Create the file:
            with open(filepath, "w+") as file:
                yaml.safe_dump(settings, file)
        else:
            # Append the user to the file:
            with open(filepath, "a+") as file:
                yaml.safe_dump(settings, file)
                file.write("\n")

            print("settings.yaml created.")
    print()


def make_user():
    print("Setting up the server.")
    filepath = "./core_utils/server_resources/database/users.yaml"

    # Check if user.yaml exists:
    overwrite = False
    skip = False
    if os.path.exists(filepath):
        # check if the user wants to overwrite the file:
        while True:
            user_input = input("The users file already exists. Do you want to skip user creation, overwrite the file, or append to it?\n([s]kip/[o]verwrite/[A]ppend) ").lower()
            user_input = user_input if user_input else "a"
            if user_input == "o":
                overwrite = True
                break
            elif user_input == "s":
                overwrite = False
                skip = True
                break
            elif user_input == "a":
                overwrite = False
                break

    # If the file does not exist or the user wants to overwrite it:
    if skip:
        print("Skipping user creation.")
    else:
        # Gather user input:
        name = input("Enter your given name: ")
        username = input("Enter your desired username: ")
        password = input("Enter your password: ")

        # hash the password:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_hash = pwd_context.hash(password)

        # Create the user dictionary:
        user = {
            "username": username,
            "name": name,
            "password_hash": password_hash,
            "auth_level": 2
        }
        all_users = {}
        all_users[username] = user

        if overwrite:
            # Create the file:
            with open(filepath, "w+") as file:
                yaml.safe_dump(all_users, file)
        else:
            # Append the user to the file:
            with open(filepath, "a+") as file:
                yaml.safe_dump(all_users, file)
                file.write("\n")

            print("users.yaml created.")
    print()


if __name__ == "__main__":

    # create settings file
    create_settings_file()
    make_user()