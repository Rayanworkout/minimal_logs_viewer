import json

from typing import Tuple

CONFIG_FILE = "projects.json"


def load_projects_list_from_config() -> Tuple[bool, list]:
    """
    Méthode permettant de charger et retourner
    depuis un fichier de configuration la liste des projets pour
    lesquels on souhaite étudier les logs.

    Returns:
        Tuple[bool, list]: Si succès, True + liste de projets
                           Sinon, False + message d'erreur
    """
    try:

        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            projects = config.get("projects")
            if projects is None:
                return False, [f'{CONFIG_FILE} ne contient pas la variable "projects".']

            return True, projects

    except FileNotFoundError:
        return (
            False,
            [
                f"{CONFIG_FILE} n'existe pas. Merci de créer le fichier de configuration."
            ],
        )

    except json.JSONDecodeError:
        return False, ["Le format du fichier JSON est incorrect."]
