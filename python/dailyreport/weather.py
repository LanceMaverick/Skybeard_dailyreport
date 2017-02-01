from datetime import datetime
import pyowm

def make_forecast(key, location):
    owm = pyowm.OWM(key)
    
    #current weather
    obs = owm.weather_at_place(location)
    current_obs = obs.get_weather()
    current_status = current_obs.get_detailed_status()
    current_temp = current_obs.get_temperature('celsius')['temp']

    #forecast
    #sometimes all fails... 
    forecast = None
    max_retries = 5
    retries = 0
    while not forecast:
        if retries > max_retries:
            raise Exception('Max retries reached')
        try:
            forecast = owm.daily_forecast(location)
        except KeyError:
            retries+=1
            pass

    fcs = []
    for fc in forecast.get_forecast():
        fcs.append(dict(
            status = fc.get_detailed_status(),
            temp = fc.get_temperature('celsius')['max'],
            date = datetime.fromtimestamp(
                fc.get_reference_time()).strftime('%A')))

    return dict(
            temp = current_temp,
            status = current_status,
            forecasts = fcs,)

