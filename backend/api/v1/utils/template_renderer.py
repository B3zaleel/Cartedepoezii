#!/usr/bin/python3
'''A module for rendering HTML page templates.
'''
import os
from jinja2 import Template


def render_template(template_name, **vars):
    '''Renders a template with the given name-value pairs.

    Args:
        template_name: The name of the template to render
        (without the .html extension).
        vars: The items used in the template.

    Returns:
        An expanded HTML-formatted string.
    '''
    template_path = os.path.join(
        'api',
        'v1',
        'templates',
        '{}.html'.format(template_name)
    )
    doc_full = ''
    if os.path.isfile(template_path):
        web_client_domain = os.getenv('WEB_CLIENT_DOMAIN')
        vars['web_client_domain'] = web_client_domain
        with open(template_path) as file:
            doc = Template(file.read())
            doc_full = doc.render(**vars)
    return doc_full
