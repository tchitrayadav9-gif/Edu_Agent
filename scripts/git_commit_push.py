"""
Git commit and push script using Dulwich pure-Python Git client.
"""
import os
import sys
from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def commit_and_push():
    repo = Repo(REPO_PATH)
    print(f"Repository at: {REPO_PATH}")

    # Stage all files
    porcelain.add(repo, paths=None)
    print("Staged modified and newly created files.")

    # Status check
    status = porcelain.status(repo)
    print("Status:", status)

    commit_msg = b"feat: Complete EduAgent upgrade with dedicated Learning, Career, and Mock Interview Agent workspaces, Recharts analytics, and MongoDB Atlas memory sync"
    author = b"tchitrayadav9-gif <tchitrayadav9-gif@users.noreply.github.com>"
    
    commit_sha = porcelain.commit(
        repo,
        message=commit_msg,
        author=author,
        committer=author
    )
    print(f"Committed SHA: {commit_sha.decode('ascii')}")

    # Push to remote
    try:
        porcelain.push(repo, "origin", "refs/heads/main")
        print("Successfully pushed changes to origin/main!")
    except Exception as e:
        print(f"Push notification: {e}")
        print("If credentials/PAT are required for HTTPS push, please ensure GitHub credentials are configured.")

if __name__ == "__main__":
    commit_and_push()
