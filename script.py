import requests,os
import pandas as pd
import argparse,time
from dotenv import load_dotenv
load_dotenv()
def get_weather(city_id, units):
    key = os.getenv('WEATHER_API_KEY')
    if not key:
        raise ValueError("Credencial WEATHER_API_KEY no detectada en el entorno.")
    url = f"https://pro.openweathermap.org/data/2.5/weather?id={city_id}&units={units}&appid={key}"
    response = requests.get(url)
    if response.status_code == 200:
        dic = response.json()
        dataframe = pd.json_normalize(
            dic, 
            record_path=['weather'], 
            meta=[
                ['sys','country'],['name'],['coord', 'lon'],
                ['coord', 'lat'],
                ['main', 'temp'], ['main', 'feels_like'],
                ['main', 'temp_min'], ['main', 'temp_max'],
                ['main', 'pressure'], ['main', 'humidity'],
                ['wind','speed'],['wind','deg'],
                ['wind','gust'],['main','grnd_level'],['main','sea_level']
            ],errors='ignore'
        )
        dataframe.rename(columns={"coord.lon":"longitud", "coord.lat":"latitud", "main.temp":"temp","main.feels_like":"feels_like",
                        "main.temp_min":"temp.min",	"main.temp_max":"temp_max",	"main.pressure":"pressure",
                        "main.humidity":"humidity",	"main.sea_level":"sea_level","main.grnd_level":"ground_level",
                        "sys.country":"country"},inplace=True)
        file_name = f"./csv/{city_id}_{int(time.time())}.csv"
        dataframe.to_csv(file_name,index=False)
        
    else:
        raise(Exception(f"API ERROR:{response.status_code}"))
parser = argparse.ArgumentParser(prog="Get Weather",
                                  description="Utiliza la API gratuita de Weahter API para consulta el clima de una determina ciudad")
parser.add_argument('city_id',help="id de la ciudad")
parser.add_argument('units',help="unidades: standar,metric o imperial")
args = parser.parse_args()
get_weather(args.city_id, args.units)

