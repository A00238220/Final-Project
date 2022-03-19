#adcb882ea837148878722e69044dc372
#importing modules 
import requests
from plotly.graph_objs import Scattergeo, Layout
from plotly.graph_objs import Bar
from plotly import offline
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go

#############
#Question 1a
##################

#making a list of cities to analyze
cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City',
'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'St. Catharines', 'Regina', 'St. Johns', 'Kelowna']


#looping through list to extract information about cities

citiess = []

for city in cities:
  #making an API call and storing the response
  url =f'https://api.openweathermap.org/data/2.5/weather?q={city},CA&appid=adcb882ea837148878722e69044dc372'

  #requesting information from url
  r = requests.get(url)

  #checking connection status
  #print(f"Status code: {r.status_code}")

  #store API response in a variable
  response_dict = r.json()

  #print(response_dict.keys())

  citiess.append(response_dict)

#dumping into a json File
filename = 'data.json'
with open(filename, 'w') as fobj:
  json.dump(citiess, fobj, indent = 4)


#accessing data from json file
filename = 'data.json'
with open(filename) as fobj:
  all_data = json.load(fobj)
  

#creating an empty list for temperature, longitude and latitude
temperatures, lons, lats = [], [], []

#looping through the json file to extract temperature, longitude and latitude, and appending to the empty list
for data in all_data:
  temp = data['main']['temp']
  lon = data['coord']['lon']
  lat = data['coord']['lat']
  temperatures.append(temp)
  lons.append(lon)
  lats.append(lat)

#print(f'Temperatures of cities : \n{temperatures}')

#formating and saving plot in html format
my_layout = Layout(title = 'Temperatures for Cities in Canada')
data = [{
  'type': 'scattergeo',
  'lon': lons,
  'lat': lats,  
  'marker' : {'size' : [0.1*mag for mag in temperatures],
  'color': temperatures,
  'colorscale' : 'Cividis',
  'reversescale' : True,
  'colorbar' : {'title' : 'Temperatures in Kelvin'}
  },

}]

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename = 'map1.html')


#############
#Question 1b
##################
#creating an empty list for humidity, longitude and latitude
humidities, lons, lats = [], [], []

#looping through the json file to extract temperature, longitude and latitude, and appending to the empty list
for data in all_data:
  hum = data['main']['humidity']
  lon = data['coord']['lon']
  lat = data['coord']['lat']
  humidities.append(hum)
  lons.append(lon)
  lats.append(lat)

#print(f'Humidities of cities : \n{humidities}')

#formating and saving plot in html format
my_layout = Layout(title = 'Humidities for Cities in Canada')
data = [{
  'type': 'scattergeo',
  'lon': lons,
  'lat': lats,  
  'marker' : {'size' : [0.3*mag for mag in humidities],
  'color': humidities,
  'colorscale' : 'Blackbody',
  'reversescale' : True,
  'colorbar' : {'title' : 'Humidities (g/m^3)'}
  },

}]

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename = 'map2.html')


#############
#Question 1c
##################
#setting x_values
x_values = cities

#creating empty lists
labels, temps, hums = [], [], []

#looping through the json file to extract labels, temperature and humidity, and appending to the empty list
for data in all_data:
  name = data['name']
  labels.append(name)
  t = data['main']['temp']
  temps.append(t)
  h = data['main']['humidity']
  hums.append(h)

#setting y_values
y_values1 = temps
y_values2 = hums

#creating an array using the numpy library
x = np.arange(len(labels))

#setting width between bars
w = 0.25

#creating plot
fig, ax1 = plt.subplots(figsize = (15, 9))

# making a plot of the second yaxis
ax2 = ax1.twinx()

#formatting plot and tick labels
ax1.bar(x - w/2, y_values1, w, color = 'blue', label = 'temperatures', align = 'edge')
ax2.bar(x + w/2, y_values2, w, color = 'green', label = 'humidities', align = 'edge')
plt.title('Cluster Bar Chart of Temperatures & Humidities for Cities in Canada ')
ax1.set_ylabel('Temperature (kelvin)')
ax2.set_ylabel('Humidity (g.kg^(-1))')
ax1.set_xlabel('Cities')
ax1.legend(['Temperature'], loc = 'upper left')
ax2.legend(['Humidity'], loc = 'upper right')
plt.xticks(x, labels)
for tick in ax1.get_xticklabels():
  tick.set_rotation(50)

#saving plot in png format
plt.savefig('clusterbarchart.png', bbox_inches = 'tight')


##############
#Question 2
########################
#creating an empty list of weather descriptions
desc = []

#looping through the json file to extract weather description, and appending to the empty list
for data in all_data:
  des = data['weather'][0]['description']
  desc.append(des)

#print(f'Weather Description:\n{desc}')

#creating an empty list for frequency
frequencies = {}

#creating key, value pairs for weather description and count of weather description
for city in desc:
  if city in frequencies:
    frequencies[city] +=1
  else:
    frequencies[city] = 1

#converting dictionary to list and setting x_values and y_values
x_valuesbar = list(frequencies.keys())
y_valuesbar = list(frequencies.values())

#creating bar plot and formatting
data = [Bar(x = x_valuesbar, y = y_valuesbar)]
x_axis_config = {'title' : 'weather description'}
y_axis_config = {'title' : 'Frequencies'}
my_layout = Layout(title = 'Frequency of Weather Description for Cities in Canada', xaxis = x_axis_config, yaxis = y_axis_config)

#saving plot in html format
offline.plot({'data': data, 'layout': my_layout}, filename = 'weatherdesc.html')

##############
#Question 3
########################

#cfreating empty lists
windspeeds, citiess = [], []

#looping through json file to extract windspeed and cities, and appending to empty list
for value in all_data:
  windspeed = value['wind']['speed']
  city = value['name']
  windspeeds.append(windspeed)
  citiess.append(city)

#print(f'Wind Speed:\n{windspeeds}')

#calculating maximum and minimum for windspeeds
maximum = max(windspeeds)
minimum = min(windspeeds)

#creating an empty dictionary
city_speed = {}

#setting counter to zero 
counter = 0

#looping through the cities list and creating key, value pairs for cities and windspeed
for city in citiess:
  city_speed[city] = windspeeds[counter]
  counter += 1

#looping through dictionary to print keys and values using an f-string
for key, value in city_speed.items():
  if value == maximum:
    print(f"The city with the maximum wind speed, with a wind speed of {value}km/h is {key} ")
  elif value == minimum:
    print(f"The city with the minimum wind speed, with a wind speed of {value}km/h is {key} ")


##############
#Question 4
########################

#creating empty lists
cities, sunrise, sunset = [], [], []

#looping through json file to extract cities, sunrise, and sunset values, and appending to empty list
for value in all_data:
  sunr = int(value['sys']['sunrise'])
  suns = int(value['sys']['sunset'])
  name = value['name']
  sunrise.append(sunr)
  sunset.append(suns)
  cities.append(name)

#creating a list to hold their difference
difference = []

#zipping both list to calculate the difference
zip_object = zip(sunset, sunrise)
for list1, list2 in zip_object:
  difference.append(list1 - list2)

#print(difference)

#creating sunduraions empty list
sundurations = []

#looping through the difference list to convert UNIX format to UTC time, and appending to the empty list
for value in difference:
  timestamp = datetime.utcfromtimestamp(value).strftime('%H:%M')
  sundurations.append(timestamp)

#print(sundurations)

#creating an empty dictionary 
city_dur = {}

#setting counter to zero
counter = 0

#looping through the cities list and creating key, value pairs for cities and sundurations
for city in cities:
  city_dur[city] = sundurations[counter]
  counter += 1

#looping through dictionary to print keys and values using an f-string to print out the duration of sunlight for each city
for key, value in city_dur.items():
  print(f'\n\nThe duration of light today, in {key}, was {value[:2]} hours and {value[3:]} minutes')

#creating a function fo calculate average length of day
def avgtime(timestringlist):
  minutecounts = []
  for val in timestringlist:
    h = val[:2]
    m = val[3:5]
    total_minutes = (int(h)*60) + int(m)
    minutecounts.append(total_minutes)
  avgtimemins = sum(minutecounts)/len(minutecounts)
  hours = int(avgtimemins/60)
  minutes = avgtimemins % 60
  return f"{hours} hours and {minutes} minutes"

#printing average duration of sunlight in all 20 cities
print(f'\nThe average length of day for all the cities is: {avgtime(sundurations)}')


##############
#Question 5
########################

#creating empty list
cities, atemps, ftemps = [], [], []

#looping through json file to extract cities, temperature, and humidity, and appending to empty list
for value in all_data:
  city =  value['name']
  atemp = value['main']['temp']
  ftemp = value['main']['feels_like']
  cities.append(city)
  atemps.append(atemp)
  ftemps.append(ftemp)

#creating an empty list for difference in actual temp and feels-like temp
difference = []

#zipping list to calculate difference and appending to empty list
zip_object = zip(atemps, ftemps)
for list1, list2 in zip_object:
  difference.append(list1 - list2)

#print(cities)
#print(difference)

#looping through zip of cities and differences and using an f-string to print out the name of the city and difference between the actual and feel-like values
for city, diff in zip(cities, difference):
  print(f'\n\nThe difference between the actual temperature and feels-like for {city} is {diff} degrees')

#Interpretation of significance of difference
print(f"\nThe significance in the difference between the actual and feels-like temperatures vary depending on the city, e.g it's significant for Regina with 6.3 degrees difference and less significant for Toronto with 0 degree difference\nThe significance is as a result of the wind speed. please see supporting data below:")

print()
#data to back up position
windspeedss = []
for value in all_data:
  windspeed = value['wind']['speed']
  windspeedss.append(windspeed)

windspeed1 = windspeedss[0]
windspeed2 = windspeedss[17]

print(f"windspeed for Toronto: {windspeed1}\nwindspeed for Regina: {windspeed2}")
print(f'\nThis indicates that the higher the windspeed, the more significant the difference between the actual and feels-like temperature will be.')

##############
#Question 6
########################
#craeting empty list
windspeeds = []

#looping through json file to extract windspeeds, and appending to empty list
for data in all_data:
  windspeed = data['wind']['speed']
  windspeeds.append(windspeed)

#selecting windspeed for Winnipeg
winnipeg = windspeeds[6]

#Creating and formatting indicator plot
my_layout = Layout(title = 'Windspeed of Winnipeg')
data = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = winnipeg,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Wind Speed for Winnipeg"}))

fig = {'data': data, 'layout': my_layout}

#saving plot in html format
offline.plot(fig, filename = 'windspeed.html')
