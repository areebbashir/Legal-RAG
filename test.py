import os
import datetime
import subprocess

# File to update
FILENAME = "daily_commit.txt"

# Append date & time to the file
with open(FILENAME, "a") as file:
    file.write(f"Updated on {datetime.datetime.now()}\n")

# Git commands
commands = [
    ["git", "add", FILENAME],
    ["git", "commit", "-m", f"Auto commit {datetime.datetime.now().date()}"],
    ["git", "push", "origin", "main"]  # Change "main" if using a different branch
]

for cmd in commands:
    subprocess.run(cmd, check=True)

print("Commit successful!")