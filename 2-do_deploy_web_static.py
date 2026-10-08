#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers using do_deploy.
"""
from fabric.api import env, put, run
import os

# Define target server IPs
env.hosts = ['52.55.249.213', '54.157.32.137']


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split('.')[0]
        remote_tmp_path = f"/tmp/{file_name}"
        release_path = f"/data/web_static/releases/{folder_name}"

        # Upload archive
        put(archive_path, remote_tmp_path)

        # Unpack archive
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf {remote_tmp_path} -C {release_path}/")
        run(f"rm {remote_tmp_path}")

        # Organize directory structure
        run(f"mv {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")

        # Update symlink
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path}/ /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception:
        return False
