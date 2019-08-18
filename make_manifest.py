def generate_deps_info(deps: list):
    for dep in deps:
        pkg_info = subprocess.check_output(["pkg", "search", "-e", "-S", "name", "-Q", "full", dep])
        origins_info = [line for line in pkg_info.decode('UTF-8').split('\n') if 'Origin' in line]
        for origin in origins_info:
            print(origin.split(':')[1].strip())
        versions_info = [line for line in pkg_info.decode('UTF-8').split('\n') if 'Version' in line]
        for version in versions_info:
            print(version.split(':')[1].strip())

with open('META_DEPENDENCIES', 'r') as md:
    meta_deps = [dep.rstrip('\n') for dep in md]
    generate_deps_info(meta_deps)



import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="templates")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template('filename')
outputText = template.render()
