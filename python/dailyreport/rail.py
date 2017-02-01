import os
import re
from .NatRail import RailScraper
rail_url = 'http://ojp.nationalrail.co.uk/service/'
curr_path = os.path.dirname(__file__)
stat_codes = os.path.join(curr_path, 'station_codes.json')

def check_times(out):
    natRail = RailScraper(rail_url, stat_codes)
    res1 = re.findall(r'(.+)\s(?:To|TO|to)\s(.+)', out)
    if not res1:
        res1 = re.findall(r'(.+)', out)
        From = res1[0]
        To = ''
    else:
        From, To = res1[0]
    out = natRail.makeDeptString(From, To)
    return dict(rail = out)

