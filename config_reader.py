import os
import sys


# Source - https://stackoverflow.com/a
# Posted by Rainer Niemann, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-07, License - CC BY-SA 4.0



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_config():

    with open(resource_path("config")) as file:
        data = file.read().strip().split("\n")
        variables = []
        for i in data:

            j = i.split(":")[1].strip().strip('"')

            variables.append(j)
    return variables[0], variables[1], variables[2]


