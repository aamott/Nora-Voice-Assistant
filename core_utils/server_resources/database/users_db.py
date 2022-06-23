###############################
# Users Database
# Stores and Loads users to and from a yaml file.
###############################
import yaml
from yaml.loader import SafeLoader
from typing import Union
from os.path import dirname

# put the database file right next to this file
DEFAULT_DB_FILENAME = dirname(__file__) + "/users.yaml"

class UserDatabase:

    def __init__(self, filename: str = DEFAULT_DB_FILENAME):
        print(filename)
        self._filename = filename

        # make sure file exists
        with open(self._filename, "a+"):
            pass

        with open(self._filename, "r") as file:
            self.users = yaml.safe_load(file)

        if not type(self.users) is dict:
            self.users = {}


    def get_users(self) -> dict:
        """Returns the users as a dictionary. 
            Returns: dict
        """
        return self.users


    def get_user(self, username:str) -> Union[dict, None]:
        """ Gets a user by username
            Returns: dict of user data
                        or None if no users found or invalid input
        """
        if not type(username) is str:
            return None

        for key in self.users:
            print("User: ",user)
            if username == self.users[key].get("username"):
                return user
        return None


    def username_is_unique(self, username:str):
        for user in self.users:
            if username == user.username:
                return False
        return True


    def add_user(self, username:str, name:str, password_hash:str, auth_level:int = 0) -> bool:
        # check that all values are valid:
        if not (type(username) is str and type(name) is str and
                type(password_hash) is str and type(auth_level) is int):
            return False

        # check that username is unique
        if not self.username_is_unique(username):
            return False

        # create the new user
        new_user_data = {
            "username": username,
            "name": name,
            "password_hash": password_hash,
            "auth_level": auth_level
        }

        # add the new user to the database
        self.users[username] = (new_user_data)

        # save
        # TODO: it would be better to save on a timer and on kill
        self.save()

        return True


    def save(self):
        with open(self._filename, "w") as file:
            self.users = yaml.safe_dump(self.users, file)


##############
# Testing
##############
if __name__ == "__main__":
    temp_filename = "temp_users.yaml"
    user_db = UserDatabase(temp_filename)

    # add an invalid user
    print()
    result = user_db.add_user(username=None, name=None, password_hash=None)
    print("Result of adding invalid user: ", result)

    # add a valid user
    result = user_db.add_user(username="doe123",
                              name="John Does",
                              password_hash="fakehashedsecret")
    print("Result of adding valid user: ", result)

    print()
    print("Test Searching:")
    user = user_db.get_user(username=None)
    print("Result of searching for None:", user)
    user = user_db.get_user(username="doe123")
    print("Result of searching for created user:", user)

    print()
    users = user_db.get_users()
    print("All users:\n", users)

    # cleanup
    print()
    from os import remove
    print("Removing temp file")
    remove(temp_filename)