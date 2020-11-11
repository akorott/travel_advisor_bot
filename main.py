import praw
import os
import weather_test
import geograpy
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


country_list = ['afghanistan', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos', 'colombia', 'comoros', 'congo', 'cook islands', 'costa rica', 'croatia', 'cuba', 'curaãƒâ§ao', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'vatican', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'isle of man', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'palestine, state of', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'romania', 'russian federation', 'rwanda', 'saint helena, ascension and tristan da cunha', 'saint kitts and nevis', 'saint lucia', 'saint martin', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and the south sandwich islands', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor-leste', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela', 'viet nam', 'virgin islands', 'wallis and futuna', 'western sahara', 'yemen', 'zambia', 'zimbabwe']

month_list = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'july', 'august', 'aug', 'september', 'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec']

# Parse post title/description for country, city and month/season

my_reddit_obj = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    username=os.environ.get("reddit_username"),
    password=os.environ.get("reddit_password"),
    user_agent="travel_advisor"
)

# target_country = []
target_city = []

robot_speech = "Hi, the historical weather forecast for the cities you're planning to visit is below  "

def extract_city(body_of_post):
    page = body_of_post

    city = geograpy.get_place_context(text=page)

    real_city = city.cities
    return real_city


# Check to see if a country appears in the post title
for submission in my_reddit_obj.subreddit('travel').new(limit=10):
    if ('2021' in submission.title) or ('2021' in submission.selftext):
        post_body = submission.selftext
        city_body = extract_city(post_body)

        post_title = submission.title
        city_title = extract_city(post_title)

        all_cities = city_body + city_title
        all_cities = set(all_cities)

        # Check if list of cities contains a country. If so, drop the "city"
        all_cities_final = []
        for city in all_cities:
            if city.lower() in country_list:
                continue
            else:
                all_cities_final.append(city)

        if all_cities_final:
            print(all_cities_final, "ALL CITIES")

        # Check if post title or body contain a month -
        months = []
        for word in submission.title.split():
            if word.lower() in month_list:
                months.append(word)
        for word in submission.selftext.split():
            if word.lower().strip() in month_list:
                months.append(word)

        print(months, "MONTHS")

        # Only take the first month for now
        if len(months) > 0:
            months = months[0]

            for city in all_cities_final:
                print(city, months)
                resp = requests.get(f'https://weather-and-climate.com/{city}-{months}-averages')
                if resp.status_code == 200:
                    URL = f'https://weather-and-climate.com/{city}-{months}-averages'
                    soup = BeautifulSoup(urlopen(URL), 'lxml')
                    submission.reply(f'{robot_speech}\n{weather_test.forecast_details(city,months)}')

