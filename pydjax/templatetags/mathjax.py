import json

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def mathjax_scripts():
    if not getattr(settings, 'MATHJAX_ENABLED', False):
        return ''

    mathjax_local_path = getattr(settings, 'MATHJAX_LOCAL_PATH', None)
    cdn_path = '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js'

    mathjax_js_url = static(
        f'{mathjax_local_path}/MathJax.js'
    ) if mathjax_local_path else cdn_path

    mathjax_config_file = getattr(settings, 'MATHJAX_CONFIG_FILE', "TeX-AMS-MML_HTMLorMML")
    url = f'{mathjax_js_url}?config={mathjax_config_file}'
    load_script_tag = f'<script type="text/javascript" src="{url}"></script>'

    mathjax_config_data = getattr(settings, 'MATHJAX_CONFIG_DATA', None)
    config_script_tag = ''
    
    if mathjax_config_data:
        config_script_tag = '<script type="text/javascript">'
        config_script_tag += 'MathJax.Hub.Config('
        config_script_tag += json.dumps(mathjax_config_data)
        config_script_tag += ');'
        config_script_tag += '</script>'

    return mark_safe(load_script_tag + config_script_tag)
