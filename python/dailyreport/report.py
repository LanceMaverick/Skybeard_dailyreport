from telegraph import Telegraph
from .pagegenerator import TGGenerator
from .weather import make_forecast
from .feeds import get_feed_elements
from .rail import check_times
from .config import telegraph_key, owm_key

def generate_report(user_config):
    tg = TGGenerator(key = telegraph_key)
    elements = dict(user = user_config['user'])
    elements.update(make_forecast(
            key = owm_key,
            location = user_config['location']))
    elements.update(get_feed_elements(user_config['feeds']))
    elements.update(check_times(user_config['journey']))
    tg.elements = elements
    response = tg.create_page('Daily Report')
    return response


    
    


    



        




    


