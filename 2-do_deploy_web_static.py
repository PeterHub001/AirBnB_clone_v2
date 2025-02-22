#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that
       distributes an archive to your web servers
Returns False if the file at the path archive_path doesn't exist
"""
import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
env.hosts = ["54.175.59.46", "35.153.79.133"]


def do_deploy(archive_path):
    """ script that distributes archive to web servers
    All remote commands must be executed on your both web servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    Returns True if all operations has been done correctly,
            otherwise returns False
    """
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        """Upload the archive to the /tmp/ directory of the web server"""
        put(archive_path, "/tmp/")
        unpack = archive_path.split("/")[-1]
        folder = ("/data/web_static/releases/" + unpack.split(".")[0])
        run("sudo mkdir -p {:s}".format(folder))

        """Uncompress the archive to the folder
        /data/web_static/releases/<archive filename without extension>
        on the web server"""
        run("sudo tar -xzf /tmp/{:s} -C {:s}".format(unpack, folder))

        """Delete the archive from the web server"""
        run("sudo rm /tmp/{:s}".format(unpack))
        run("sudo mv {:s}/web_static/* {:s}/".format(folder, folder))
        run("sudo rm -rf {:s}/web_static".format(folder))

        """Delete the symbolic link /data/web_static/current"""
        run('sudo rm -rf /data/web_static/current')

        """Create a new the symbolic link
           /data/web_static/current on the web server, linked to the new
           version of your code
           (/data/web_static/releases/<archive filename without extension>)"""
        run("sudo ln -s {:s} /data/web_static/current".format(folder))
        return True
    except:
        return False
