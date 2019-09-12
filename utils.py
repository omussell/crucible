import jinja2

def jinja_template(filename, *args):
    template_loader = jinja2.FileSystemLoader(searchpath="templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(filename)
    outputText = template.render(args)

from jinja2 import Environment, FileSystemLoader
 
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=True,
    loader=FileSystemLoader('templates')
    )
 
 
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
 
 
def create_index_html():
    fname = "output.html"
    #urls = ['http://example.com/1', 'http://example.com/2', 'http://example.com/3']
    context = {
        'deps': { 
            'tmux': {
                'origin': 'asdf',
                'version': '1.1.1'
            },
            'vim-console': {
                'origin': 'asdf',
                'version': '1.1.1'
            }
        },
    }
    #
    with open(fname, 'w') as f:
        html = render_template('DEPENDENCIES', context)
        f.write(html)
 
 
def main():
    create_index_html()
