# Plot Covid data for comparing countries

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

def getSmoothData(continent, country, nDaySmooth=14):
    """
    Read in Covid19 deaths per day and return array of dates and array
    of deaths per population smoothed with a nDaySmooth running mean for a
    particular country in a particular continent
    """
    
    # Read in data
    data=np.genfromtxt('continents/'+continent+'/'+country+'.dat',
                   delimiter=' ', dtype=None, names=True,
                   skip_header=0, usecols=(1,2,3,4,5,6))
    
    # Separate data into 1d arrays per day
    days = data['day']
    months = data['month']
    years = data['year']
    popData = data['popData2019']
    cases = data['cases']
    deaths = data['deaths']
    
    # A list of dates
    dates = [dt.date(years[i], months[i], days[i]) for i in range(len(data))]
    
    # nDaySmooth day average of deaths
    deathsSmooth = deaths[nDaySmooth-1:]
    for i in range(nDaySmooth-1):
        deathsSmooth = deathsSmooth + deaths[i:-nDaySmooth+i+1]
    deathsSmooth = deathsSmooth / nDaySmooth /popData[0]
    if nDaySmooth == 1:
        datesSmooth = dates.copy()
    else:
        datesSmooth = dates[int(np.floor((nDaySmooth-1)/2)):-int(np.floor(nDaySmooth/2))]
    
    return datesSmooth, deathsSmooth

[UKdates, UKdeaths] = getSmoothData('Europe', 'United_Kingdom',nDaySmooth=14)
[Italydates, Italydeaths] = getSmoothData('Europe', 'Italy',nDaySmooth=14)
[Chinadates, Chinadeaths] = getSmoothData('Asia', 'China',nDaySmooth=14)
[USAdates, USAdeaths] = getSmoothData('America', 'United_States_of_America',nDaySmooth=14)
[Indiadates, Indiadeaths] = getSmoothData('Asia', 'India',nDaySmooth=14)
[Brazildates, Brazildeaths] = getSmoothData('America', 'Brazil',nDaySmooth=14)

#Make deaths per 100 million population
UKdeaths *= 1e8
Italydeaths *= 1e8
Chinadeaths *= 1e8
USAdeaths *= 1e8
Indiadeaths *= 1e8
Brazildeaths *= 1e8

# Plot and save
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
plt.plot(UKdates, UKdeaths, 'k', label='UK')
plt.plot(Italydates, Italydeaths, 'r', label='Italy')
plt.plot(Chinadates, Chinadeaths, 'b', label='China')
plt.plot(USAdates, USAdeaths, 'c', label='USA')
plt.plot(Indiadates, Indiadeaths, 'm', label='India')
plt.plot(Brazildates, Brazildeaths, 'g', label='Brazil')
plt.legend()
plt.title("Deaths per day per 100 million population, 14 day mean")
plt.gcf().autofmt_xdate()
plt.savefig("output/countryDeaths.pdf")

