import os
import json
import subprocess
from git import Repo


MAIN_BRANCH = "main"
REPO_PATH = "/opt/codebase/monorepo"
CICD_PATH = os.path.join(REPO_PATH, "cicd")
META_FILE_NAME = "meta.json"
PROJECT_CONFIG_FILENAME = "project_config.json"

repo = Repo(REPO_PATH)

def command(args):
    sp = subprocess.run(
        args
    )
    return sp

def get_status(repo, path):
    changed = [item.a_path for item in repo.index.diff(MAIN_BRANCH)]
    if path in repo.untracked_files:
        return "untracked"
    elif path in changed:
        return "modified"
    else:
        return "na"

def search_meta(path):
    meta_file = os.path.join(path, META_FILE_NAME)
    exist_meta = os.path.exists(meta_file)
    if exist_meta:
        return meta_file
    else:
        if path == REPO_PATH:
            return None
        return search_meta(os.path.dirname(path))

def load_json(meta_file):
    f = open(meta_file)
    data = json.load(f)
    return data

def search_updated_projects():
    updated_projects = []
    for item in repo.index.diff(MAIN_BRANCH):
        status = get_status(repo, item.a_path)
        if status == "modified":
            file_path = os.path.join(REPO_PATH, item.a_path)
            modified_path = os.path.dirname(file_path)
            meta_file = search_meta(modified_path)
            if meta_file is not None:
                info = load_json(meta_file)
                updated_projects.append(info["name"])
    return updated_projects

def get_project_config(project_id):
    project_config_path = os.path.join(CICD_PATH, PROJECT_CONFIG_FILENAME)
    project_config_json = load_json(project_config_path)
    for project_config in project_config_json["projects"]:
        if project_id == project_config["id"]:
            return project_config
    return None

def build_project(project):
    command(['build.sh', project])

def deploy_project(project):
    command(['deploy.sh', project])

projects = search_updated_projects()

for project in projects:
    project_config = get_project_config(project)
    if project_config is not None:
        build_project(project_config["id"])
        deploy_project(project_config["id"])
