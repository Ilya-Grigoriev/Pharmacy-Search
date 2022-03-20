import sys
from io import BytesIO
import requests
from PIL import Image
from distance import lonlat_distance

place = input('Введите адрес: ')
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": place,
    "format": "json"}
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
place_coord = toponym["Point"]["pos"]
lon, lat = place_coord.split()

metro_request = 'https://search-maps.yandex.ru/v1/'
params = {
    'apikey': '611ec11a-6b32-42d2-8883-40ffb48f0ef0',
    'lang': 'ru_RU',
    'text': 'аптека',
    'll': ','.join([lon, lat])
}
response = requests.get(metro_request, params=params).json()
pharmacy = response['features'][0]
pharmacy_coord = list(map(str, pharmacy['geometry']['coordinates']))
pharmacy_address = pharmacy['properties']['description']
pharmacy_name = pharmacy['properties']['name']
pharmacy_work = pharmacy['properties']['CompanyMetaData']['Hours']['text']
print(f'Адрес аптеки: {pharmacy_address}')
print(f'Название аптеки: {pharmacy_name}')
print(f'График работы аптеки: {pharmacy_work}')
map_params = {
    "l": "map",
    'pl': f'{",".join(pharmacy_coord)},{",".join([lon, lat])}',
    'pt': f'{",".join(pharmacy_coord)},pm2dbm1~{",".join([lon, lat])},pm2rdm2'
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
print(f'Расстояние от адреса до аптеки: {lonlat_distance(map(float, pharmacy_coord), map(float, [lon, lat]))}')
