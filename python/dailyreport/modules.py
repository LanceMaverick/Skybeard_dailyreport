from telegraph import Telegraph
from weather import make_forecast
import config

#proof of concept
def weather():
    key = config.owm_key
    loc = config.location
    w = make_forecast(key, loc)
    elements = ["<h3>Weather Forecasts</h3>"]
    elements.append("""<p>The weather is currently {} with a temperature
    of <b>{}</b> degrees celsius.</p>""".format(w['status'], str(int(w['temp']))))
    elements.append("<p> While the forecast for the following week is:</p>")
    elements.append("<ul>")
    fcs = w["forecasts"]
    for fc in fcs:
        elements.append("<li><b>{}:</b> {}, {}C</li>".format(
            fc['date'],
            fc['status'],
            fc['temp']))

    return elements



if __name__ =="__main__":
    elements = ['<p>Good Morning Peter. Here is your daily report.</p>']
    elements+=weather()

    tph = Telegraph(access_token = config.telegraph_key)
    response = tph.create_page('Daily Report', html_content=''.join(elements))
    print(response)
    



        




    


