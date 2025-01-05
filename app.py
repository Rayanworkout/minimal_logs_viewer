import argparse
import os
import pandas as pd


from flask import Flask, render_template, request, jsonify, current_app
from helpers import load_projects_list_from_config

app = Flask(__name__)


@app.route("/")
def home():
    not_found_projets = []
    found_projects = []
    config_error = None

    is_production = current_app.config.get("production", False)

    success, PROJECTS = load_projects_list_from_config(is_production=is_production)

    if not success:
        config_error = PROJECTS[0]

        return render_template(
            "index.html",
            projects=[],
            project_folders_errors=", ".join(not_found_projets),
            config_error=config_error,
        )

    for project in PROJECTS:
        if (
            not os.path.isdir(project)
            or not os.path.exists(project)
            or not os.path.exists(os.path.join(project, "logs"))
        ):
            not_found_projets.append(project)
        else:
            found_projects.append(project)

    not_found_projets = [f'"{p}"' for p in not_found_projets]
    projects = [(p, os.path.basename(p)) for p in found_projects]
    return render_template(
        "index.html",
        projects=projects,
        project_folders_errors=", ".join(not_found_projets),
        config_error=config_error,
    )


@app.route("/get_logs", methods=["POST"])
def get_logs():
    data = request.get_json()
    project = data.get("project")

    if not project:
        return jsonify({"success": False, "message": "Project not found"}), 400

    LOG_DIR = os.path.join(project, "logs")

    if not os.path.exists(LOG_DIR):
        return (
            jsonify({"success": False, "message": "This project has no logs folder"}),
            400,
        )

    log_files = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]

    if not log_files:
        return (
            jsonify(
                {"success": False, "message": "No log files found in this project"}
            ),
            400,
        )

    logs = ""

    for log in log_files:
        with open(os.path.join(LOG_DIR, log)) as f:
            log_content = f.readlines()
            logs += "\n\n".join([line.strip() for line in log_content])

    # Convert to DataFrame if needed
    as_df = data.get("as_df", False)
    if as_df:
        logs = convert_to_df(logs)

    return jsonify({"success": True, "log_content": logs})


def convert_to_df(logs: str):
    """
    Fonction permettant de convertir les logs en df
    pour les afficher sous forme de tableau.

    Args:
        logs (str): Les logs au format str.
    """
    # Convert the logs into a list of lines
    log_lines = logs.strip().split("\n")

    # Parse the log lines into a structured format
    data = []
    for line in log_lines:
        if "---------------" in line:
            continue  # Skip dashed lines
        parts = line.split(" - ")
        if len(parts) == 7:
            date_time, level, server, session_id, duration, script, status = parts
            data.append(
                {
                    "Date_Time": date_time,
                    "Level": level,
                    "Host": server,
                    "Run_ID": session_id,
                    "Duration": float(duration),
                    "Script": script,
                    "Status": status,
                }
            )

    # Create a DataFrame
    df = pd.DataFrame(data)
    print(df)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run the Flask app with optional configurations."
    )
    parser.add_argument(
        "--prod",
        type=lambda x: True if x == "1" else False,
        default=0,
        help="Run the app in production mode (1 or 0).",
    )

    prod = parser.parse_args().prod
    app.config["production"] = prod
    print(f"Production: {prod}")
    app.run(host="0.0.0.0")
