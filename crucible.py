subprocess.run(['zfs', 'list', '-t', 'filesystem', '-H', '-o', 'name', '-s', 'name'])
