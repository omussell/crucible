#subprocess.run(['zfs', 'list', '-t', 'filesystem', '-H', '-o', 'name', '-s', 'name'])


import requests
import subprocess
from pathlib import Path

#url = f"{settings.base_file_url}"
url = 'https://download.freebsd.org/ftp/releases/amd64/amd64/12.0-RELEASE/base.txz'
r = requests.get(url, stream=True)

# download base.txz if not already exists
local_file = f"{settings.base_file_path}/base-{url.split('/')[-2]}.txz"
if not Path(local_file).is_file():
    with open(local_file, 'wb') as fd:
        chunk_size = 1024 * 1024
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


# update to latest patch version
subprocess.run(['freebsd-update', '-b', '/usr/local/jails/taiga', '--not-running-from-cron', 'fetch'], stdout=subprocess.DEVNULL)
