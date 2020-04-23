from fabric import task
import random
import hashlib
import socket
from pathlib import Path
from fabfile import zfs


#@task
#def get(c):
#    print("get ze jails")
#
#
## directory subtree
## hostname
## ip address
#
## start
## stop
## restart
#
## template
#
#
## jail

@task
def create_jail_ip(name):
    # Convert name to bytestring so it can be used with random.seed
    byte_name = name.encode('UTF-8')
    # Create hash of name for use as a different seed. Otherwise both numbers are the same or close
    hash_name = hashlib.sha3_256(byte_name).hexdigest().encode('UTF-8')

    random.seed(byte_name)
    ip1 = random.randrange(0, 255)
    random.seed(hash_name)
    ip2 = random.randrange(2, 254)

    return f"192.168.{ip1}.{ip2}"

def create_jail_conf(name):
    jail_ip = create_jail_ip(name)
    jail_conf_template = f"""
exec.prestart = "";
exec.start = "/bin/sh /etc/rc";
exec.poststart = "";
exec.prestop ="";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.poststop = "";
exec.clean;
#mount.devfs;
path = "/usr/local/jails/$name";
interface="lo1";
#allow.mount;
#allow.mount.devfs;
host.hostname = $name;

{name} {{ ip4.addr = {jail_ip}; }}
   """
   jail_conf_path = Path(f"{jails_mount}/conf")
   jail_conf_path.mkdir(parents=True, exist_ok=True)
   with open(f"{jail_conf_path}/jail.{name}.conf", "w") as jail_conf:
       jail_conf.write(jail_conf_template)

@task
def jail_start(c, name):
    """Start jail(s)."""
    c.sudo(f"jail -q -f /etc/jail.conf -c {name}")

@task
def jail_create(c, name, clone_dataset, snapshot):

    # Jail names cant have "." characters or be uppercase
    name = name.replace(".", "-").lower()

    create_jail_conf(name)
    zfs.clone_create(c, clone_dataset, snapshot, f"tank/jails/{name}")
    jail_start(c, name)


@task(optional=["name"])
def jail_get(c, name=None):
    """Get list of jails."""
    if name:
        c.run(f"jls -j {name} name")
    else:
        c.run("jls")

#
#
#@task
#def jail_start(c, jail_conf=str, name=str):
#    """Start a jail."""
#    print('wtf')
#    #c.run(f"jls")
#    c.run(f"jail -c {name}")




#jail_conf = f"""
#interface = "re0";
#host.hostname = "$name";
#ip4.addr = 192.168.1.$ip;
#path = "/usr/local/jails/$name";
#
#exec.start = "/bin/sh /etc/rc";
#exec.stop = "/bin/sh /etc/rc.shutdown";
#exec.clean;
##mount.devfs;
#
## Jail Definitions
#{jailname} {
#    $ip = {jailip};
#}
#"""
