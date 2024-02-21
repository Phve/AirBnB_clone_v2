#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ['54.86.220.207', '54.175.137.217']

@runs_once
def create_archive():
    """Create a tar gzipped archive of the directory web_static."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Creating web_static archive: {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static archive created: {} -> {} Bytes".format(output, archive_size))
        return output
    except Exception as e:
        print("Error creating archive:", e)
        return None

def deploy_archive(archive_path):
    """Deploy the static files to the host servers."""
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed successfully!')
        return True
    except Exception as e:
        print("Error deploying archive:", e)
        return False

def deploy():
    """Create and deploy the static files to the host servers."""
    archive_path = create_archive()
    if archive_path:
        return deploy_archive(archive_path)
    else:
        return False
