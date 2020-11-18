import praw
import os
import geograpy
import requests
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

# List of countries copied from github: https://gist.github.com/kalinchernev/486393efcca01623b18d
country_list = ['afghanistan', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos', 'colombia', 'comoros', 'congo', 'cook islands', 'costa rica', 'croatia', 'cuba', 'curaãƒâ§ao', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'vatican', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'palestine, state of', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'romania', 'russian federation', 'rwanda', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis', 'saint lucia', 'saint martin', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela', 'viet nam', 'virgin islands', 'wallis and futuna', 'western sahara', 'yemen', 'zambia', 'zimbabwe']

# List of months
month_list = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'july', 'august', 'aug', 'september', 'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec']

bot_name = 'weather_buddy'

my_reddit_obj = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    username=os.environ.get("reddit_username"),
    password=os.environ.get("reddit_password"),
    user_agent="weather_buddy"
)

# Text posted by bot at the beginning of every comment submitted
robot_intro = "*beep beep boop - I'm the weather buddy*" + "\n\nHistorical weather forecast for your trip:"

# Instantiate a subreddit object from my_reddit_obj
subreddit = my_reddit_obj.subreddit('travel')

# Checks to see if a month is included either in the title or body of post.
def month_checker(title, body):
    months = []
    for word in title.split():
        if word.lower().strip('.,') in month_list:
            months.append(word)
    for word in body.split():
        if word.lower().strip('.,') in month_list:
            months.append(word.strip('.,'))
    return months

# Function that parses cities from any text using the geograpy module
def extract_city(text):
    city = geograpy.get_place_context(text=text)
    real_city = city.cities
    return real_city

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

# Check to see if a country appears in the post title
while True:
    for submission in subreddit.new(limit=1000):
        all_authors = []
        if ('2021' in submission.title) or ('2021' in submission.selftext):
            print(submission.title)
            for comment in submission.comments:
                all_authors.append(str(comment.author))

            # Ensure the bot hasn't already made a comment in the post.
            if bot_name not in all_authors:
                # city_body/city_title return a list of cities found in the title/body of the post
                post_body = submission.selftext
                city_body = extract_city(post_body)

                post_title = submission.title
                city_title = extract_city(post_title)

                all_cities = city_body + city_title

                # Remove duplicate cities
                all_cities = set(all_cities)

                # The geograpy module isn't perfect and sometimes incorrectly labels a country as a city. Drop any countries from the list of cities.
                only_cities = []
                for city in all_cities:
                    if city.lower() in country_list:
                        continue
                    else:
                        only_cities.append(city)

                # If one or more cities were found in the post then continue.
                if only_cities:

                    # Check if the post title or body contains a month
                    months = month_checker(title=submission.title, body=submission.selftext)

                    # Only provide results for the first month. I may come back and add a functionality for multiple months in the future.
                    # Make sure that the post includes both, a month and at least one city.

                    if months and only_cities:
                        months = months[0]
                        # good_cities are cities that returned a response code of 200 and exist on the weather-and-climate website.
                        good_cities = []
                        for city in only_cities:
                            resp = requests.get(f'https://weather-and-climate.com/{city}-{months}-averages')
                            if resp.status_code == 200:
                                good_cities.append(city)

                        if good_cities:
                            time.sleep(1000)
                            reply_string = ''
                            for i in range(len(good_cities)):
                                reply_string += f"\n{forecast_details(good_cities[i],months)}"

                            print(robot_intro + reply_string)
                            submission.reply(robot_intro + reply_string)
    time.sleep(60)


# ISSUE IS THAT AFTER CHECKING RESPOSNE, ONE CITY IS REMOVED BUT NOT THE SECOND. WHY?!