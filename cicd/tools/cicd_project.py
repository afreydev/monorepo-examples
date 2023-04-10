import os
import json
import subprocess
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from git import Repo

META_FILE_NAME = "meta.json"
PROJECT_CONFIG_FILENAME = "project_config.json"
LAST_COMMIT = "HEAD~1"

def command(args):
    sp = subprocess.run(
        args
    )
    return sp

def get_status(repo, path, commit = LAST_COMMIT):
    changed = [item.a_path for item in repo.index.diff(commit)]
    if path in repo.untracked_files:
        return "untracked"
    elif path in changed:
        return "modified"
    else:
        return "na"

def search_meta(repo_path, path):
    meta_file = os.path.join(path, META_FILE_NAME)
    exist_meta = os.path.exists(meta_file)
    if exist_meta:
        return meta_file
    else:
        if path == repo_path:
            return None
        return search_meta(repo_path, os.path.dirname(path))

def load_json(meta_file):
    f = open(meta_file)
    data = json.load(f)
    return data

def search_updated_projects(repo_path, commit = LAST_COMMIT):
    repo = Repo(repo_path)
    updated_projects = []
    for item in repo.index.diff(commit):
        status = get_status(repo, item.a_path)
        if status == "modified":
            file_path = os.path.join(repo_path, item.a_path)
            modified_path = os.path.dirname(file_path)
            meta_file = search_meta(repo_path, modified_path)
            if meta_file is not None:
                info = load_json(meta_file)
                updated_projects.append(info["name"])
    return updated_projects

def get_project_config(repo_path, project_id):
    cicd_path = os.path.join(repo_path, "cicd")
    project_config_path = os.path.join(cicd_path, PROJECT_CONFIG_FILENAME)
    project_config_json = load_json(project_config_path)
    for project_config in project_config_json["projects"]:
        if project_id == project_config["id"]:
            return project_config
    return None

def build_project(project):
    command(['build.sh', project])

def deploy_project(project):
    command(['deploy.sh', project])

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--commit", help="Commit or branch name", default=LAST_COMMIT)
parser.add_argument("-d", "--docker", help="Is it running in docker?", action='store_true')
args = vars(parser.parse_args())
commit = args["commit"]
docker = args["docker"]

REPO_PATH = "/home/runner/work/monorepo-examples/monorepo-examples"

if docker:
    REPO_PATH = "/opt/codebase/monorepo"

projects = search_updated_projects(REPO_PATH, commit)

for project in projects:
    project_config = get_project_config(REPO_PATH, project)
    if project_config is not None:
        build_project(project_config["id"])
        deploy_project(project_config["id"])
