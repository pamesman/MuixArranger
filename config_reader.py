from pathlib import Path
def get_config():

    with open("config") as file:
        data = file.read().strip().split("\n")
        variables = []
        for i in data:

            j = i.split(":")[1].strip().strip('"')

            variables.append(j)
    return variables[0], variables[1], variables[2]


