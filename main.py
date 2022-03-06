import requests
import folium
from pyfiglet import Figlet


def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}').json()

        return {
            'country': response.get('country'),
            'region': response.get('region'),
            'region_name': response.get('regionName'),
            'city': response.get('city'),
            'zip': response.get('zip'),
            'lat': response.get('lat'),
            'lon': response.get('lon'),
            'provider': response.get('isp'),
            'org': response.get('org'),
            'ip': response.get('query')
        }
    except requests.exceptions.ConnectionError:
        print('[!] Please check your connection!')
    except requests.exceptions.JSONDecodeError:
        print('[!] JSON encoding error')


def main():
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('IP INFO'))

    user_ip = input('Please enter your ip: ')
    info_from_ip = get_info_by_ip(user_ip)

    lat = info_from_ip.get('lat')
    lon = info_from_ip.get('lon')
    m = folium.Map(location=[lat, lon])

    m.save('index.html')


if __name__ == '__main__':
    main()
