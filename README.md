# CRUCIBLE

Build applications using Python and ZFS

When Pkgbase is released, can also be used for building ZFS Boot Environments.

## Create a template

A ZFS dataset is created using the base files from FreeBSD. You can change the FreeBSD version in the settings. The files are updated to the latest patch version.

The template package can then be installed into the template. The template package is a FreeBSD package which contains the dependencies and files needded in the template.

Once complete, a snapshot is taken of the dataset.

## Clone template

When a new container is required, a clone of the template snapshot is taken. By default, this is the most recent snapshot but this can be overridden in the settings.

The new dataset name needs to be given (when used by CI, this would include the Git commit hash in the name).

## Start jails

A new jail.conf file is created specifically for this jail, then started using `jail -c -f jail.$HASH.conf`.

## Build application

Install dependencies as specified in the meta manifest, build the application using the Makefile, then create a new FreeBSD package containing the dependencies and the application files.

## create MANIFEST files

For the template package and application package, a MANIFEST file needs to exist. To create this, a META_DEPENDENCIES file contains a human-readable list of packages. Then the make_manifest.py will iterate over that list, and query the pkg repos to get the correct versions and info to build the MANIFEST file. Call the MANIFEST file the DEPENDENCIES file instead so its clearer that its only installing deps not the MANIFEST for the application itself.
using jinja template to populate the files.
(jinja templates can also be used for nginx upstream files and jail-$jail.conf files)
