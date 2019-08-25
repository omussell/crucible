import subprocess

#def get_pkg_info(dep: str):
#    pkg_info = subprocess.check_output(["pkg", "search", "-e", "-S", "name", "-Q", "full", dep])

def generate_dep_origin(dep: str):
    pkg_info = subprocess.check_output(["pkg", "search", "-e", "-S", "name", "-Q", "full", dep])
    origins_info = [line for line in pkg_info.decode('UTF-8').split('\n') if 'Origin' in line]
    for origin in origins_info:
        deps_origin = origin.split(':')[1].strip()
    return deps_origin

def generate_dep_version(dep: str):
    pkg_info = subprocess.check_output(["pkg", "search", "-e", "-S", "name", "-Q", "full", dep])
    versions_info = [line for line in pkg_info.decode('UTF-8').split('\n') if 'Version' in line]
    for version in versions_info:
        deps_version = version.split(':')[1].strip()
    return deps_version

deps_dict = {}
for dep in deps:
    deps_dict[dep] = {}
    deps_dict[dep]['origin'] = generate_dep_origin(dep)
    deps_dict[dep]['version'] = generate_dep_version(dep)

template.render()



deps = ['tmux']
generate_deps_info(deps)

#with open('META_DEPENDENCIES', 'r') as md:
#    meta_deps = [dep.rstrip('\n') for dep in md]
#    generate_deps_info(meta_deps)
#
#
#
#import jinja2
#
#template_loader = jinja2.FileSystemLoader(searchpath="templates")
#template_env = jinja2.Environment(loader=template_loader)
#template = template_env.get_template('filename')
#outputText = template.render()
