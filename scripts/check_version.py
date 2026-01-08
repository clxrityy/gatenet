"""
Fail if Git tag version != pyproject.toml version
"""

import sys
import tomllib
import subprocess

def get_git_tag():
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--exact-match"],
            stderr=subprocess.DEVNULL
        ).decode().strip().lstrip("v")
    except subprocess.CalledProcessError:
        return None

def get_pyproject_version():
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)["project"]["version"]

tag = get_git_tag()
py_version = get_pyproject_version()

if tag is None:
    print("No Git tag found - Skipping version check.")
    sys.exit(0)

if tag != py_version:
    print(f"ERROR: git tag ({tag}) does not match pyproject.toml version ({py_version})")
    sys.exit(1)

print(f"VERSION CHECK PASSED: {tag}")
