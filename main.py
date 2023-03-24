import requests
from requests_html import HTMLSession
import json

s = HTMLSession()
API_URL = "http://localhost:5000/Weather/"

print("Welcome to the Weather Scraping from Google to database!")

def scrap_weather():
    query = input("Type the city or country : ")
    url = f'https://www.google.com/search?q=weather+{query}'
    r = s.get(url, headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    try:
        name = (r.html.find('div.eKPi4 span.BBwThe',first=True).text).upper()
        temp = r.html.find('span#wob_tm', first=True).text
        unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
        date = r.html.find('div.wob_dts', first=True).text
        desc = r.html.find('div.wob_dcp', first=True).find('span#wob_dc', first=True).text
        print(name,temp,unit,date,desc)

        # Create a dictionary to store the weather data
        weather_data = {
            'name': name,
            'temp': temp,
            'unit': unit,
            'date': date,
            'desc': desc
        }

        # Send a POST request to the API to add the weather data to the database
        response = requests.post(API_URL + name, json=weather_data)
        if response.status_code == 201:
            print(f"{name} weather data added to the database!")
            print("_______________________________________")

        elif response.status_code == 403 :
            print("Error: This country or City is taken!")
            print("_______________________________________")
        else:
            print("Error: Failed to add weather data to the database!")
            print("_______________________________________")
    
    except:
        print("This City or Country does not exist in our world!")
        print("_______________________________________")

def get_weather():
    countryName = input("Please type the country or the city name : ").upper()
    response = requests.get(API_URL + countryName)
    if response.status_code == 200:
        data = json.loads(response.content)
        if data:
            print(f"Name: {data['name']}")
            print(f"Temperature: {data['temp']}{data['unit']}")
            print(f"Date: {data['date']}")
            print(f"Description: {data['desc']}")
            print("_______________________________________")
    else:
        print("This Country or City does not exist in the database!")
        print("_______________________________________")

def get_all():
    response = requests.get(API_URL + "All")
    if response.status_code == 200:
        datas = json.loads(response.content)
        if datas:
            for data in datas:
                print(f"Name: {data['name']}")
                print(f"Temperature: {data['temp']}{data['unit']}")
                print(f"Date: {data['date']}")
                print(f"Description: {data['desc']}")
                print("_______________________________________")
        else :
            print("There nothing here, In database!")
            print("_______________________________________")


def delete():
    weather_name = input("Enter the name to delete: ").upper()
    response = requests.delete(API_URL + weather_name)
    if response.status_code == 404:
        print(f"Name : '{weather_name}' not found in the database.")
        print("_______________________________________")
    else:
        print(f"Name : '{weather_name}' deleted.")
        print("_______________________________________")

while True : 
    print("Please choose the number")
    print("1. Scrap the weather from Google")
    print("2. See the weather from database")
    print("3. See all the weather from database")
    print("4. Delete a Weather")
    print("5. Quit the program")
    try :
        num_input = int(input("Type here : "))

        if num_input == 1:
            scrap_weather()

        elif num_input == 2:
            get_weather()

        elif num_input == 3 :
            get_all()

        elif num_input == 4:
            delete()

        elif num_input == 5:
            break
    except:
        print("Invalid input! Please choose a number from the list.")
        print("_______________________________________")
