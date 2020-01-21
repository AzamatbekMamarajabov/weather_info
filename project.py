import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dbconnect import select_city_by_id, insert_weather, select_weather_by_city, create_connection
WEATHER_API = 'https://api.darksky.net/forecast/7ddb1a5069c2f255075f68d5e146cd0d/'

import requests

first_arg = sys.argv[1]

def get_weather(query):

    results = {}

    city = select_city_by_id(query)
    lat = city[2]
    lon = city[3]
    print(lat)
    print(lon)

    url = WEATHER_API+lat+','+lon

    try:
        results = requests.get(url)
        
    except requests.ConnectionError as exception:
        return f'{exception}'
    return results


def weather_parse(query):

    json_all = query.json()

    time = json_all['currently']['time']
    summary = json_all['currently']['summary']
    windSpeed = json_all['currently']['windSpeed']
    temperature = json_all['currently']['temperature']
    uvIndex = json_all['currently']['uvIndex']
    visibility = json_all['currently']['visibility']

    return time, summary, windSpeed, temperature, uvIndex, visibility



if __name__ == '__main__':
    database = os.path.join(basedir, 'data.db')

    # create a database connection
    conn = create_connection(database)


    city_id =first_arg
    city_id = int(city_id)
    resp = get_weather(city_id)

    time, summary, windSpeed, temperature, uvIndex, visibility = weather_parse(resp)
    result = (time, summary, windSpeed, temperature, uvIndex, visibility, city_id )
    
    if conn is not None:
        insert_weather(conn,result)

    with conn:

        print(" Query all weather")
        select_weather_by_city(conn, city_id)