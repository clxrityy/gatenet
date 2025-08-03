#!/usr/bin/env python3
"""
Delete all empty files in the project directory tree.

Usage:
    python3 scripts/delete_empty_files.py

Deletes any file (not directory) with size == 0 bytes.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def delete_empty_files(root: str):
    count = 0
    exclude = os.path.join(root, "src", "gatenet", "__init__.py")
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                if os.path.isfile(fpath) and os.path.getsize(fpath) == 0 and os.path.abspath(fpath) != os.path.abspath(exclude):
                    os.remove(fpath)
                    print(f"Deleted empty file: {fpath}")
                    count += 1
            except Exception as e:
                print(f"Error deleting {fpath}: {e}")
    print(f"Total empty files deleted: {count}")

if __name__ == "__main__":
    delete_empty_files(ROOT)
