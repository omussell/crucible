import subprocess
import tarfile
from pathlib import Path
from shutil import copyfile

import requests
from fabric import task


@task
def base_template_create(c, freebsdversion):
    """Create a new base template."""

    jails_mount = '/usr/local/jails'
    url = f"https://download.freebsd.org/ftp/releases/amd64/amd64/{freebsdversion}-RELEASE/base.txz"
    base_file = f"{jails_mount}/base-{url.split('/')[-2]}.txz"
    template_mount = f"{jails_mount}/template-{freebsdversion}"
    pkg_prefix = f"env ASSUME_ALWAYS_YES=YES pkg -r {template_mount}"

    def download_base_file(url, base_file):
        r = requests.get(url, stream=True)

        print("Downloading base file")
        # download base.txz if not already exists
        if not Path(base_file).is_file():
            with open(base_file, 'wb') as fd:
                chunk_size = 1024 * 1024
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)

    def extract_base_to_template(template_mount, base_file):
        print("Extracting base file")
        if not Path(f"{template_mount}/root").is_dir():
            with tarfile.open(base_file) as tar:
                tar.extractall(path=template_mount)

    def patch_base(template_mount):
        print("Patching base template")
        # update to latest patch version
        subprocess.run(['freebsd-update', '-b', template_mount, '--not-running-from-cron', 'fetch', 'install'], stdout=subprocess.DEVNULL)

    def copy_files_from_host(template_mount):
        print("Copying files from host")
        host_files = [
        # To allow DNS resolution within jail
            "/etc/resolv.conf",
        # Without these files some package installs may fail (like puppet)
            "/etc/passwd",
            "/etc/group",
        ]
        for host_file in host_files:
            copyfile(host_file, f"{template_mount}/{host_file}")

    def custom_files(template_mount):
        print("Creating custom files")
        rc_conf_content = """
            sendmail_enable="NO"
            sendmail_submit_enable="NO"
            sendmail_outbound_enable="NO"
            sendmail_msp_queue_enable="NO"
        """
        with open(f"{template_mount}/etc/rc.conf", "w") as rc_conf:
            rc_conf.write(rc_conf_content)

    def bootstrap_pkg():
        print("Bootstrapping pkg")
        subprocess.run(f"{pkg_prefix} install -qy pkg", shell=True)

    def bootstrap_puppet():
        print("Bootstrapping puppet")
        subprocess.run(f"{pkg_prefix} install -qy puppet5", shell=True)

    def install_pkg_deps():
        print("Installing package dependencies")
        install_packages = [
            "git-lite",
            "htop",
            "bash",
        ]
        for package in install_packages:
            subprocess.run(f"{pkg_prefix} install -qy {package}", shell=True)

    print("Creating template dataset")
    c.run(f"zfs create -p -o mountpoint={template_mount} tank/jails/template-{freebsdversion}", shell='/bin/sh')
    download_base_file(url, base_file)
    extract_base_to_template(template_mount, base_file)
    patch_base(template_mount)
    copy_files_from_host(template_mount)
    custom_files(template_mount)
    bootstrap_pkg()
    bootstrap_puppet()
    install_pkg_deps()
