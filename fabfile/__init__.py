from invoke import Collection

import fabfile.jail
import fabfile.zfs
import fabfile.pkg

ns = Collection()
ns.add_collection(jail)
ns.add_collection(zfs)
ns.add_collection(pkg)
