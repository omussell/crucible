BOX_NAME = "freebsd/FreeBSD-12.1-RELEASE"
ZFS_DISK = './zfs_disk.vdi'

$script = <<-SCRIPT
sudo pkg install -y py37-virtualenvwrapper python3 vim-console
if test ! -d /home/vagrant/.virtualenvs; then mkdir -p /home/vagrant/.virtualenvs; fi
if test ! -d /home/vagrant/.virtualenvs/crucible; then python3 -m virtualenv -p `which python3` /home/vagrant/.virtualenvs/crucible; fi
/home/vagrant/.virtualenvs/crucible/bin/pip install -r /home/vagrant/crucible/requirements.txt
if test -z "`grep 'source .virtualenvs/crucible/bin/activate.csh' /home/vagrant/.cshrc`"; then echo "source .virtualenvs/crucible/bin/activate.csh" >> /home/vagrant/.cshrc ; fi
if test -z "`grep 'cd crucible/' /home/vagrant/.cshrc`"; then echo "cd crucible/" >> /home/vagrant/.cshrc ; fi
SCRIPT

$zfs_script = <<-ZFS
sysrc zfs_enable="YES"
service zfs start
/bin/sh -c 'if ! `zpool list | grep -q "tank"`; then zpool create tank /dev/ada1; fi'
/bin/sh -c 'if ! `zfs list | grep -q "tank/jails"`; then zfs create -o mountpoint=/usr/local/jails tank/jails; fi'
ZFS

Vagrant.configure("2") do |config|

    config.vm.hostname = "crucible-vagrant"
    config.vm.box = BOX_NAME

    # Create is needed on the shared folder or the mount fails the first time
    config.vm.synced_folder ".", "/home/vagrant/crucible", type: "virtualbox", :automount => true, :create => true

    config.vm.provider "virtualbox" do |vb|
      vb.cpus = 4
      vb.memory = 4096
      vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
      vb.customize ["modifyvm", :id, "--audio", "none"]
      vb.customize ["modifyvm", :id, "--ioapic", "on"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]

      unless File.exist?(ZFS_DISK)
        vb.customize ['createhd', '--filename', ZFS_DISK, '--size', 20 * 1024]
      end
      vb.customize ['storageattach', :id, '--storagectl', 'IDE Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--nonrotational', 'on', '--medium', ZFS_DISK]
    end

    config.ssh.shell = "sh"
    config.ssh.forward_agent = true
    config.vm.guest = :freebsd
    config.vm.provision "shell", inline: $zfs_script
    config.vm.provision "shell", inline: $script, privileged: false

end
