#!/usr/bin/python2

# Kindle Weather Display
# Stephan Ruttloff (http://www.ruttloff.org)
# based on work from  Matthew Petroff (http://www.mpetroff.net/)
# 01/2013

import urllib2
from xml.dom import minidom
import datetime
import codecs

#
# Download and parse weather data
#

# Fetch data (change lat and lon to desired location)
weather_xml = urllib2.urlopen('http://weather.yahooapis.com/forecastrss?w=643134&u=c').read()
dom = minidom.parseString(weather_xml)

yweather = 'http://xml.weather.yahoo.com/ns/rss/1.0'

city = dom.getElementsByTagNameNS(yweather, 'location')[0].getAttributeNode('city').nodeValue

unit_temp   = dom.getElementsByTagNameNS(yweather, 'units')[0].getAttributeNode('temperature').nodeValue
unit_dist   = dom.getElementsByTagNameNS(yweather, 'units')[0].getAttributeNode('distance').nodeValue
unit_prsr   = dom.getElementsByTagNameNS(yweather, 'units')[0].getAttributeNode('pressure').nodeValue
unit_speed  = dom.getElementsByTagNameNS(yweather, 'units')[0].getAttributeNode('speed').nodeValue

condition_text  = dom.getElementsByTagNameNS(yweather, 'condition')[0].getAttributeNode('text').nodeValue
condition_code  = dom.getElementsByTagNameNS(yweather, 'condition')[0].getAttributeNode('code').nodeValue
condition_temp  = dom.getElementsByTagNameNS(yweather, 'condition')[0].getAttributeNode('temp').nodeValue
condition_date  = dom.getElementsByTagNameNS(yweather, 'condition')[0].getAttributeNode('date').nodeValue

forecasts   = dom.getElementsByTagNameNS(yweather, 'forecast')

forecast_day    = [None]*2
forecast_date   = [None]*2
forecast_low    = [None]*2
forecast_high   = [None]*2
forecast_text   = [None]*2
forecast_code   = [None]*2

for i in range(len(forecasts)):
    forecast_day[i]     = forecasts[i].getAttributeNode('day').nodeValue
    forecast_date[i]    = forecasts[i].getAttributeNode('date').nodeValue
    forecast_low[i]     = forecasts[i].getAttributeNode('low').nodeValue
    forecast_high[i]    = forecasts[i].getAttributeNode('high').nodeValue
    forecast_text[i]    = forecasts[i].getAttributeNode('text').nodeValue
    forecast_code[i]    = forecasts[i].getAttributeNode('code').nodeValue

output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

output = output.replace('CITY_NAME',city)
output = output.replace('UNIT_TEMP',unit_temp)

icons = [None]*49
icons[0] = "ra"                 #tornado
icons[1] = "ra"                 #tropical storm
icons[2] = "ra"                 #hurricane
icons[3] = "tsra"               #severe thunderstorms
icons[4] = "tsra"               #thunderstorms
icons[5] = "rasn"               #mixed rain and snow
icons[6] = "ip"                 #mixed rain and sleet
icons[7] = "mix"                #mixed snow and sleet
icons[8] = "shra"               #freezing drizzle
icons[9] = "shra"               #drizzle
icons[10] = "freezing_rain"     #freezing rain
icons[11] = "ra"                #showers
icons[12] = "ra"                #showers
icons[13] = "snow"              #snow flurries
icons[14] = "rasn"              #light snow showers
icons[15] = "blizzard"          #blowing snow
icons[16] = "snow"              #snow
icons[17] = "ip"                #hail
icons[18] = "ip"                #sleet
icons[19] = "dust"              #dust
icons[20] = "foggy"             #foggy
icons[21] = "foggy"             #haze
icons[22] = "foggy"             #smoky
icons[23] = "wind"              #blustery
icons[24] = "wind"              #windy
icons[25] = "cold"              #cold
icons[26] = "ovc"               #cloudy
icons[27] = "cloudy"            #mostly cloudy (night)
icons[28] = "cloudy"            #mostly cloudy (day)
icons[29] = "sct"               #partly cloudy (night)
icons[30] = "sct"               #partly cloudy (day)
icons[31] = "clear_night"       #clear (night)
icons[32] = "skc"               #sunny
icons[33] = "sunny_few_clouds"  #fair (night)
icons[34] = "sunny_few_clouds"  #fair (day)
icons[35] = "raip"              #mixed rain and hail
icons[36] = "hot"               #hot
icons[37] = "tsra"              #isolated thunderstorms
icons[38] = "scttsra"           #scattered thunderstorms
icons[39] = "scttsra"           #scattered thunderstorms
icons[40] = "hi_shwrs"          #scattered showers
icons[41] = "snow"              #heavy snow
icons[42] = "rasn"              #scattered snow showers
icons[43] = "snow"              #heavy snow
icons[44] = "sunny_few_clouds"  #partly cloudy
icons[45] = "tsra"              #thundershowers
icons[46] = "snow"              #snow showers
icons[47] = "tsra"              #isolated thundershowers
icons[48] = "unknown"           #not available (3200)

if (int(condition_code) < 0) or (int(condition_code) > 47):
    condition_icon = icons[48]
else:
    condition_icon = icons[int(condition_code)]

forecast_icon = [None]*2

if (int(forecast_code[0]) < 0) or (int(forecast_code[0]) > 47):
    forecast_icon[0] = icons[48]
else:
    forecast_icon[0] = icons[int(forecast_code[0])]

if (int(forecast_code[1]) < 0) or (int(forecast_code[1]) > 47):
    forecast_icon[1] = icons[48]
else:
    forecast_icon[1] = icons[int(forecast_code[1])]

# AKTUELL
output = output.replace('CURRENT_TMP',condition_temp)
output = output.replace('ICON_ONE',condition_icon)

# MORGEN
output = output.replace('DAY_TWO',forecast_day[0])
output = output.replace('LOW_TWO',forecast_low[0])
output = output.replace('HIGH_TWO',forecast_high[0])
output = output.replace('ICON_TWO',forecast_icon[0])

# UEBERMORGEN
output = output.replace('DAY_THREE',forecast_day[1])
output = output.replace('LOW_THREE',forecast_low[1])
output = output.replace('HIGH_THREE',forecast_high[1])
output = output.replace('ICON_THREE',forecast_icon[1])

codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)