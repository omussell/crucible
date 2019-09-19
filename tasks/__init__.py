from invoke import Collection

import tasks.zfs

ns = Collection()
ns.add_collection(zfs)
