#############################
# Skill Creator
# Creates instances of skills in the skills folder.
#############################
SKILLS_FOLDER = "skills"

import importlib
import os


def import_skills():
    """ Imports all skills. """
    # import the skills
    skills = []

    skill_module_paths = get_skill_module_paths()
    for module_path in skill_module_paths:
        try:
            skill_module = import_skill(module_path)
            skill = skill_module.Skill()
        except Exception as e: 
            print("Error importing skill: " + module_path)
            print(e)

        skills.append(skill)

    return skills


##################
# Helper functions
##################

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
                    skill_module_paths.append(SKILLS_FOLDER +'.' + file + "." + subfile)

    return skill_module_paths


def import_skill(module_path):
    """ Imports a skill module. """
    # import the skill
    skill_module = importlib.import_module(module_path)
    return skill_module