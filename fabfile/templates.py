## DEPENDENCIES 
#name: FIXME
#version: FIXME
#origin: FIXME
#comment: FIXME
#www: FIXME
#maintainer: FIXME
#prefix: /usr/local
#desc: <<EOD
#   FIXME 
#EOD
#deps: {
#{% for k,v in deps.items() %}
#    {{ k }}: {{ v|safe }}
#{%- endfor %}
#}


jail_conf = f"""
interface = "re0";
host.hostname = "$name";
ip4.addr = 192.168.1.$ip;
path = "/usr/local/jails/$name";

exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
#mount.devfs;

# Jail Definitions
{jailname} {
    $ip = {jailip};
}
"""
