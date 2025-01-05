import json
import os

from typing import Tuple


def load_projects_list_from_config(is_production: bool) -> Tuple[bool, list]:
    """
    Méthode permettant de charger et retourner
    depuis un fichier de configuration la liste des projets pour
    lesquels on souhaite étudier les logs.

    Returns:
        Tuple[bool, list]: Si succès, True + liste de projets
                           Sinon, False + message d'erreur
    """

    CONFIG_FILE_BASE_PATH = (
        r"C:\Python\python_runner_logs_viewer" if is_production else "."
    )
    CONFIG_FILE = os.path.join(CONFIG_FILE_BASE_PATH, "projects.json")
    
    try:

        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            projects = config.get("projects")
            if projects is None:
                return False, [f'{CONFIG_FILE} ne contient pas la variable "projects".']

            if len(projects) < 1:
                return False, [
                    "aucun projet n'est mentionné dans le fichier de configuration."
                ]

            return True, projects

    except FileNotFoundError:
        return (
            False,
            [
                f"{CONFIG_FILE} n'existe pas. Merci de créer le fichier de configuration."
            ],
        )

    except json.JSONDecodeError:
        return False, ["le format du fichier JSON est incorrect."]
