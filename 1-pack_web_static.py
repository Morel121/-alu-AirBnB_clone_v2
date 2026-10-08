#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repository.
"""
from fabric.api import local
from datetime import datetime
import os


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
