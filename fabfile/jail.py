from fabric import task


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
@task(optional=["name"])
def jail_get(c, name=None):
    """Get list of jails."""
    if name:
        c.run(f"jls -j {name} name")
    else:
        c.run("jls")

@task(optional=["name"])
def jail_start(c, name=None):
    """Start jail(s)."""
    if name:
        c.sudo(f"jail -q -f /etc/jail.conf -c {name}")
    #else:
    #    c.sudo("jail -c")
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
