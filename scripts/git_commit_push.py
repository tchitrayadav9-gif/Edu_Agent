"""
Git commit and push script using Dulwich pure-Python Git client and Windows Credential Manager.
"""
import os
import sys
import ctypes
import ctypes.wintypes
import urllib.parse
from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', ctypes.wintypes.DWORD),
        ('Type', ctypes.wintypes.DWORD),
        ('TargetName', ctypes.c_wchar_p),
        ('Comment', ctypes.c_wchar_p),
        ('LastWritten', ctypes.wintypes.FILETIME),
        ('CredentialBlobSize', ctypes.wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', ctypes.wintypes.DWORD),
        ('AttributeCount', ctypes.wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', ctypes.c_wchar_p),
        ('UserName', ctypes.c_wchar_p),
    ]

PCREDENTIAL = ctypes.POINTER(CREDENTIAL)
advapi32 = ctypes.windll.Advapi32

CredRead = advapi32.CredReadW
CredRead.argtypes = [ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD, ctypes.POINTER(PCREDENTIAL)]
CredRead.restype = ctypes.wintypes.BOOL

CredFree = advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]

def get_github_credential():
    for target in ['git:https://github.com', 'LegacyGeneric:target=git:https://github.com', 'https://github.com']:
        pcred = PCREDENTIAL()
        res = CredRead(target, 1, 0, ctypes.byref(pcred))
        if res and pcred:
            cred = pcred.contents
            user = cred.UserName or 'tchitrayadav9-gif'
            size = cred.CredentialBlobSize
            raw_blob = ctypes.string_at(cred.CredentialBlob, size)
            try:
                pwd = raw_blob.decode('utf-16-le')
            except Exception:
                pwd = raw_blob.decode('utf-8', errors='ignore')
            CredFree(pcred)
            return user, pwd
    return None, None

def commit_and_push():
    repo = Repo(REPO_PATH)
    print(f"Repository at: {REPO_PATH}")

    # Stage all files
    porcelain.add(repo, paths=None)
    print("Staged modified and newly created files.")

    commit_msg = b"feat: Complete Learning Agent redesign with personalized subject platform, verified resources, topic learning screen, EduMind AI assistant, and career bridge"
    author = b"tchitrayadav9-gif <tchitrayadav9-gif@users.noreply.github.com>"
    
    try:
        commit_sha = porcelain.commit(
            repo,
            message=commit_msg,
            author=author,
            committer=author
        )
        print(f"Committed SHA: {commit_sha.decode('ascii')}")
    except Exception as e:
        print(f"Commit note: {e}")

    # Push with credentials
    user, token = get_github_credential()
    if user and token:
        safe_user = urllib.parse.quote(user, safe='')
        safe_token = urllib.parse.quote(token, safe='')
        auth_url = f"https://{safe_user}:{safe_token}@github.com/tchitrayadav9-gif/Edu_Agent.git"
        print("Pushing to GitHub remote via authenticated HTTPS endpoint...")
        try:
            porcelain.push(repo, auth_url, "refs/heads/main")
            print(">>> SUCCESS: Pushed all code and commits to GitHub repo (main branch)!")
        except Exception as e:
            print(f"Push error: {e}")
    else:
        print("No stored Windows credential found for git:https://github.com")

if __name__ == "__main__":
    commit_and_push()
