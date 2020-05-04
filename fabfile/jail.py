from fabric import task
import random
import hashlib
import socket
from pathlib import Path
from fabfile import zfs

# Local means fabric is being run with the intention of creating jails locally like on BuildBot
# Remote means fabric is connecting via SSH to another server and starting jails there

jails_mount = "/usr/local/jails"

@task
def create_jail_ip(c, name):
    # Convert name to bytestring so it can be used with random.seed
    byte_name = name.encode('UTF-8')
    # Create hash of name for use as a different seed. Otherwise both numbers are the same or close
    hash_name = hashlib.sha3_256(byte_name).hexdigest().encode('UTF-8')

    random.seed(byte_name)
    ip1 = random.randrange(0, 255)
    random.seed(hash_name)
    ip2 = random.randrange(2, 254)

    return f"192.168.{ip1}.{ip2}"

@task
def create_jail_conf_template(c, name):
    jail_ip = create_jail_ip(c, name)
    jail_conf_template = f"""
exec.prestart = "";
exec.start = "/bin/sh /etc/rc";
exec.poststart = "";
exec.prestop ="";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.poststop = "";
exec.clean;
#mount.devfs;
path = "{jails_mount}/$name";
interface="lo1";
#allow.mount;
#allow.mount.devfs;
host.hostname = $name;

{name} {{ ip4.addr = {jail_ip}; }}
"""
    return jail_conf_template


@task
def local_create_jail_conf(c, name):
    jail_conf_template = create_jail_conf_template(c, name)
    jail_conf_path = Path(f"{jails_mount}/conf")
    jail_conf_path.mkdir(parents=True, exist_ok=True)
    with open(f"{jail_conf_path}/jail.{name}.conf", "w") as jail_conf:
        jail_conf.write(jail_conf_template)

@task
def remote_create_jail_conf(c, name):
    jail_conf_template = create_jail_conf_template(c, name)
    #jail_conf_path = Path(f"{jails_mount}/conf")
    #jail_conf_path.mkdir(parents=True, exist_ok=True)
    with open(f"jail.{name}.conf", "w") as jail_conf:
        jail_conf.write(jail_conf_template)
    c.put(jail_conf, remote=f"{jails_mount}/conf/jail.{name}.conf")
    Path(f"jail.{name}.conf").unlink()

@task
def local_jail_name(c, app, ver):
    # Jail names cant have "." characters or be uppercase
    clean_ver = ver.replace(".", "-").lower()
    jail_name = f"{app}-{clean_ver}"

@task
def remote_jail_name(c, app, env, ver):
    hostname = c.run("hostname -s").stdout.strip("\n")
    # Jail names cant have "." characters or be uppercase
    clean_ver = ver.replace(".", "-").lower()
    jail_name = f"{hostname}-jail-{app}-{clean_ver}"
    return jail_name

@task
def local_jail_start(c, name):
    """Start jail(s)."""
    jails_mount = "/usr/local/jails"
    c.run(f"jail -q -f {jails_mount}/conf/jail.{name}.conf -c {name}")

@task
def remote_jail_start(c, name):
    """Start jail(s)."""
    jails_mount = "/usr/local/jails"
    c.sudo(f"jail -q -f {jails_mount}/conf/jail.{name}.conf -c {name}")


@task
def local_jail_create(c, clonedataset, app, ver):

    name = local_jail_name(c, app, ver)
    latest_snapshot = zfs.snapshot_get_latest(c, clonedataset)
    dataset = latest_snapshot.split('@')[0]
    snapshot = latest_snapshot.split('@')[1]

    create_jail_conf(c, name)
    zfs.clone_create(c, dataset, snapshot, f"tank/jails/{name}")
    local_jail_start(c, name)

@task
def remote_jail_create(c, app, env, ver):

    name = remote_jail_name(c, app, env, ver)

    ## download built jail
    remote_create_jail_conf(c, name)
    remote_jail_start(c, name)


@task(optional=["name"])
def jail_get(c, name=None):
    """Get list of jails."""
    if name:
        c.run(f"jls -j {name} name")
    else:
        c.run("jls")
