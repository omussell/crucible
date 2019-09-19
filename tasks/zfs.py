from invoke import task

# zpool
# zfs dataset
# zfs volume
# snapshot
# clone
# replication (send/recv)




@task
def dataset_get(c, dataset):
    print('get the datasets')
