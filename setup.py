#####################
# Setup script

##################
# Set up the user.yaml file:
import os
from passlib.context import CryptContext
import yaml

def make_user():
    # Check if user.yaml exists:
    overwrite = False
    skip = False
    filepath = "./core_utils/server_resources/database/users.yaml"
    if os.path.exists(filepath):
        # check if the user wants to overwrite the file:
        while True:
            user_input = input("The file already exists. Do you want to skip user creation, overwrite the file, or append to it?\n ([s]kip/[o]verwrite/[A]ppend) ").lower()
            user_input = user_input if user_input else "a"
            if user_input == "o":
                overwrite = True
                break
            elif user_input == "s":
                overwrite = False
                break
            elif user_input == "a":
                overwrite = False
                break

    # If the file does not exist or the user wants to overwrite it:
    if skip:
        print("Skipping user creation.")
    else:
        # Gather user input:
        name = input("Name: ")
        username = input("Username: ")
        password = input("Password: ")

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

            print("User created.")

make_user()