from fabric import task
from pathlib import Path
from fabfile import jail


@task
def create_nginx_conf(c, app, mode):
    jails_mount = "/usr/local/jails"
    jail_ip = create_jail_ip(c, name)
    jail_conf_template = f"""
upstream {app}_{mode} {{ server {jail_ip}:8000 fail_timeout=10s; }}
    """
    local_nginx_file = f"{app}_{mode}.conf"
    remote_nginx_file = f"/usr/local/etc/nginx/conf.d/{app}_{mode}-upstream.conf"
    with open(local_nginx_file, "w") as nginx_conf:
        nginx_conf.write(nginx_conf_template)
    c.put(local_nginx_file, remote=remote_nginx_file)
    Path(local_nginx_file).unlink()
