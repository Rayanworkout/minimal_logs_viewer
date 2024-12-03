import json

CONFIG_FILE = "projects.json"


def load_projects_list_from_config() -> list:
    """
    Méthode permettant de charger et retourner
    depuis un fichier de configuration la liste des projets pour
    lesquels on souhaite étudier les logs.

    Raises:
        Exception: Lorsqu'une variable du fichier de configuration est manquante.
        FileNotFoundError: Lorsque le fichier de configuration n'est pas trouvé ou n'existe pas.
        json.JSONDecodeError: Lorsque le contenu du fichier de configuration est invalide.

    Returns:
        list: La liste des variables de configuration, dans le même ordre que la liste MANDATORY_VARS.
    """
    try:

        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            projects = config.get("projects")
            if projects is None:
                raise Exception(
                    f'{CONFIG_FILE} ne contient pas la variable "projects".'
                )

            return projects

    except FileNotFoundError:
        raise FileNotFoundError(
            f"{CONFIG_FILE} n'existe pas. Merci de créer le fichier de configuration."
        )

    except json.JSONDecodeError:
        raise json.JSONDecodeError(
            f"Le format du fichier JSON est incorrect. {CONFIG_FILE}"
        )
