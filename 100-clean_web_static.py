#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""
from fabric.api import env, local, run
import os

env.hosts = ['3.93.4.225', '3.94.109.78']


def do_clean(number=0):
    """
    Deletes outdated archives locally and remotely.
    Args:
        number (int/str): Number of archives to keep (0 or 1 keeps newest 1).
    """
    try:
        number = int(number)
    except ValueError:
        return

    if number < 1:
        number = 1

    # Clean local versions folder
    if os.path.exists("versions"):
        archives = sorted(os.listdir("versions"))
        archives_to_delete = archives[:-number]
        for archive in archives_to_delete:
            local("rm -f versions/{}".format(archive))

    # Clean remote releases folder
    remote_path = "/data/web_static/releases"
    cmd = "ls -1t {} | grep '^web_static_'".format(remote_path)
    releases = run(cmd).split("\n")

    releases = [r.strip() for r in releases if r.strip()]
    releases_to_delete = releases[number:]

    for release in releases_to_delete:
        run("rm -rf {}/{}".format(remote_path, release))
