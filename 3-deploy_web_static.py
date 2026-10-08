#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['52.55.249.213', '54.157.32.137']


def do_pack():
    """Generates a .tgz archive from web_static folder."""
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"

        print(f"Packing web_static to {archive_path}")
        result = local(f"tar -cvzf {archive_path} web_static")

        if result.succeeded:
            return archive_path
        return None
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split('.')[0]
        remote_tmp_path = f"/tmp/{file_name}"
        release_path = f"/data/web_static/releases/{folder_name}"

        put(archive_path, remote_tmp_path)
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf {remote_tmp_path} -C {release_path}/")
        run(f"rm {remote_tmp_path}")
        run(f"mv {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path}/ /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Packs web_static content and deploys it to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
