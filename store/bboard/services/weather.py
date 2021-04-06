WEATHER_API_KEY = '188abfa17b9e25d458dfb0eb0fa0dcc6'
import requests
def get_weather(user):
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+user.city +'&units=metric&appid=' +WEATHER_API_KEY)
        res = res.json()
        print('')
        weather = res['weather'][0]['main']
        temp = res['main']['temp']
        return weather +', ' +str(temp)+' degrees'
    except:
        return None

