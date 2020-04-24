from invoke import Collection

import fabfile.jail
import fabfile.zfs
import fabfile.pkg
import fabfile.templates
import fabfile.nginx

ns = Collection()
ns.add_collection(jail)
ns.add_collection(zfs)
ns.add_collection(pkg)
ns.add_collection(templates)
ns.add_collection(nginx)
