#!/usr/bin/python3
"""
Fabric script to generate .tgz archive
"""

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Generates .tgz archive from the contents of the web_static folder
    """
    time = datetime.now()
    archive = 'versions/web_static_' + time.strftime("%Y%m%d%H%M%S") + '.tgz'
    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static'.format(archive))

    if result.failed:
        return None
    return archive
