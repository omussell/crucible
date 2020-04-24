from fabric import task

# zpool
# zfs dataset
# zfs volume
# snapshot
# clone
# replication (send/recv)


# zpool
@task(optional=["zpool"])
def zpool_get(c, zpool=None):
    """Get list of zpools."""
    if zpool:
        c.run(f"zpool list -H -o name {zpool}")
    else:
        c.run("zpool list -H -o name")


# dataset
@task(optional=["dataset"])
def dataset_get(c, dataset=None):
    """Get list of datasets."""
    if dataset:
        c.run(f"zfs list -t filesystem -H -o name -s name {dataset}")
    else:
        c.run("zfs list -t filesystem -H -o name -s name")


@task
def dataset_create(c, dataset):
    """Create a new dataset."""
    c.run(f"zfs create -p {dataset}")


# snapshot
@task(optional=["snapshot"])
def snapshot_get(c, snapshot=None):
    """Get a list of snapshots."""
    if snapshot:
        c.run(f"zfs list -t snapshot -H -o name -s name {snapshot}")
    else:
        c.run("zfs list -t snapshot -H -o name -s name")


@task
def snapshot_create(c, dataset, name):
    """Create a new snapshot."""
    c.run(f"zfs snapshot {dataset}@{name}")


@task
def snapshot_destroy(c, dataset, name):
    """Destroy a snapshot."""
    c.run(f"zfs destroy {dataset}@{name}")

@task
def snapshot_get_latest(c, dataset):
    """Get the most recently created snapshot."""
    c.run(f"zfs list -t snapshot -o name,creation -s creation -r {dataset} | tail -1")


# clone
#@task
#def clone_get(c):
#    print("get")

@task
def clone_create(c, clonedataset, newclone):
    """Create a clone from a snapshot."""
    dataset = snapshot_get_latest(c, clonedataset)
    c.run(f"zfs clone {dataset} {newclone}")


@task
def clone_get_snapshot(c, name):
    """Get the snapshot from which this clone was created."""
    c.run(f"zfs get -H -o value origin {name}")


# replication (send/recv)
@task
def replicate_send_remote(c, dataset, snapshot, destination_host, destination_zpool, destination_filesystem):
    c.run(f"zfs send {dataset}@{snapshot} | ssh {destination_host} zfs recv {destination_zpool}/{destination_filesystem}")

@task 
def replicate_send_file(c, dataset, filename):
    snapshot_create(c, dataset, "zfssend")
    c.run(f"zfs send {dataset}@{snapshot} | gzip > {filename}.gz")
    snapshot_destroy(c, dataset, "zfssend")
