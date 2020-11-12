from bs4 import BeautifulSoup
from urllib.request import urlopen

# beautiful soup is an HTML/CSS parser

# target_city = 'Toronto'
# target_month = 'January'

# URL = f'https://weather-and-climate.com/{target_city}-{target_month}-averages'

# soup = BeautifulSoup(urlopen(URL), 'lxml')

# min_temp = soup.find('span', class_='label', text='Min Temperature').find_next('span').text
# max_temp = soup.find('span', class_='label', text='Max Temperature').find_next('span').text
# average_precipitation = soup.find('span', class_='label', text='Precipitation').find_next('span').text
# chance_of_precipitation = soup.find('span', class_='label', text='Chance of Rain').find_next('span').text

def convert_to_fahrenheit(temp):
    celcius = int(temp.split()[0])
    fahrenheit = round(celcius * (9/5) + 32)
    return fahrenheit

def forecast_details(city,month):

    URL = f'https://weather-and-climate.com/{city}-{month}-averages'
    soup = BeautifulSoup(urlopen(URL), 'lxml')

    min_temp = soup.find('span', class_='label', text='Min Temperature').find_next('span').text
    max_temp = soup.find('span', class_='label', text='Max Temperature').find_next('span').text
    average_precipitation = soup.find('span', class_='label', text='Precipitation').find_next('span').text
    chance_of_precipitation = soup.find('span', class_='label', text='Chance of Rain').find_next('span').text

    return f'\nCity: {city}  \nMonth: {month}  \nMin Temp: {min_temp} / {convert_to_fahrenheit(min_temp)} °F  \nMax Temp: {max_temp} / {convert_to_fahrenheit(max_temp)} °F  \nAvg Monthly Precipitation: {average_precipitation}  \nDaily Chance of Precipitation: {chance_of_precipitation}'














# print(target_city[0])

# for i in range(len(target_city)):
#     forecast_details(target_city[i],target_month)

# def forecast_details(city,month):
#     print(f'City: {city}')
#     print(f'Month: {month}')
#     print(f'Minimum Temperature: {min_temp} / {convert_to_fahrenheit(min_temp)} °F')
#     print(f'Maximum Temperature: {max_temp} / {convert_to_fahrenheit(max_temp)} °F')
#     print(f'Average Monthly Precipitation: {average_precipitation}')
#     print(f'Daily Chance of Precipitation: {chance_of_precipitation}')


