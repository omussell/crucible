# This file is the actual business logic

# Create a new jail:
# if template doesnt exist, create it
# if snapshot doesnt exist, create it
# zfs create clone of snapshot
# come up with a new IP
# create new jail.$jail.conf file
# start the jail
