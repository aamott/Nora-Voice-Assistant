#############################
# Skill Creator
# Creates instances of skills in the skills folder.
#############################
SKILLS_FOLDER = "skills"

import importlib
import os
from core_utils.audio_utils import AudioUtils
from core_utils.core_core.channels import Channels

from core_utils.core_core.settings_manager import SettingsManager
from core_utils.settings_tool import SettingsTool


def import_skills(settings_manager: SettingsManager, channels: Channels, audio_utils: AudioUtils) -> list:
    """ Imports all skills. 
        Skill names must be unique.

        Returns:
            skills (list[class]): a list of skills 
    """
    # Get the skill module paths
    skills = []
    skill_module_paths = get_skill_module_paths()

    # Import the skills
    for module_path in skill_module_paths:
        try:
            # Import the skill
            skill_module = importlib.import_module(module_path)

            # Prepare tools for skill
            settings_path = "skill." + skill_module.Skill.name
            settings_tool = SettingsTool(settings_manager=settings_manager,
                                         setting_path=settings_path)

            # Create the skill
            skill = skill_module.Skill(settings_tool=settings_tool, channels=channels, audio_utils=audio_utils)
            skill.populate_settings()

            if skill_name_is_unique(skill.name, skills):
                skills.append(skill)
                print("Skill " + skill.name + " imported.")

            else:
                raise Exception("Skill name '{}' is not unique.".format(skill.name))

        except Exception as e:
            print("Error importing skill:", module_path, "Error:", e)

    return skills


##################
# Helper functions
##################

def skill_name_is_unique(skill_name, skills):
    """ Checks if a skill name is unique. """
    # check if the skill name is unique
    for skill in skills:
        if skill.name == skill_name:
            return False
    return True


def get_skill_module_paths():
    """ Gets the paths to the skill modules. """
    # get the skill module paths
    skill_module_paths = []

    for file in os.listdir(SKILLS_FOLDER):
        # import single file skills
        if file.endswith(".py"):  # or os.path.isdir(file): # modules can be in .py or in a folder with an __init__.py
            file = file.replace(".py", "")
            skill_module_paths.append(SKILLS_FOLDER + '.' + file)
        # import skill inside folders
        elif os.path.isdir(SKILLS_FOLDER + '/' + file):
            # find the entry file - should be __init__.py, init.py, or same as the folder name
            for subfile in os.listdir(SKILLS_FOLDER + '/' + file):
                if subfile == "__init__.py" or subfile == "init.py" or subfile == file:
                    subfile = subfile.replace(".py", "")
                    skill_module_paths.append(SKILLS_FOLDER +'.' + file + '.' + subfile)

    return skill_module_paths


def import_skill(module_path):
    """ Imports a skill module. """
    # import the skill
    skill_module = importlib.import_module(module_path)
    return skill_module