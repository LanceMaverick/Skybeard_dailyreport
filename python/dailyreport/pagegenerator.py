import os
from jinja2  import Template, Environment, FileSystemLoader
from telegraph import Telegraph

curr_path = os.path.dirname(__file__)

class TGGenerator:
    def __init__(self, *args, **kwargs):
        self.tg = Telegraph(access_token = kwargs['key'])
        self.elements = kwargs.get('elements', None)
        self.template_path = os.path.join(curr_path, 'skb/templates')
        self.env = Environment(autoescape=True,                                         
                loader=FileSystemLoader(self.template_path))
        self.template = self.env.get_template('template.html') 
               
    def create_page(self, title, elements = None):
        if not elements:
            if not self.elements:
                raise ValueError('No elements to render')
            else:
                elements = self.elements
            
            response = self.tg.create_page(
                    title, html_content=self.template.render(elements))
            return response
        


    
    
