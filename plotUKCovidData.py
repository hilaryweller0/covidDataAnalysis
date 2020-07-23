# Plot Covid data for the UK

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

# Read in data
data=np.genfromtxt('continents/Europe/United_Kingdom.dat', delimiter=' ',
                   dtype=None, names=True,
                   skip_header=0, usecols=(1,2,3,4,5,6))

# Separate data into 1d arrays per day
days = data['day']
months = data['month']
years = data['year']
cases = data['cases']
deaths = data['deaths']

# A list of dates
dates = [dt.date(years[i], months[i], days[i]) for i in range(len(data))]

# 14 day average of deaths
nDays = 14
deathsSmooth = deaths[nDays-1:]
for i in range(nDays-1):
    deathsSmooth = deathsSmooth + deaths[i:-nDays+i+1]
deathsSmooth = deathsSmooth / nDays
datesSmooth = dates[int(nDays/2):-int(nDays/2)+1]

# Plot and save
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
plt.bar(dates, deaths)
plt.plot(datesSmooth, deathsSmooth, 'k', label='14 day average')
plt.legend()
plt.title("UK Covid19 deaths per day")
plt.gcf().autofmt_xdate()
plt.savefig("output/UKdeaths.pdf")
plt.show()

