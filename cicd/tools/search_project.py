from git import Repo


repo = Repo("/opt/codebase/monorepo")

def get_status(repo, path):
    changed = [item.a_path for item in repo.index.diff(None)]
    if path in repo.untracked_files:
        return "untracked"
    elif path in changed:
        return "modified"
    else:
        return "don't care"

for item in repo.index.diff(None):
    print(item.a_path)
    #get_status(repo, )