# Plot Covid data for comparing countries

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy.signal import savgol_filter

def binomcoeffs(n): 
    return (np.poly1d([0.5, 0.5])**n).coeffs

def getSmoothData(continent, country, nSmooth):
    """
    Read in Covid19 deaths per day and return array of dates and array
    of deaths per population smoothed with a binomial filter of width nSmooth
    for a particular country in a particular continent
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
    cases = data['cases']/popData
    deaths = data['deaths']/popData
    
    # A list of dates (as ints)
    day0 = dt.date(2020,1,1)
    dates = [dt.date(years[i], months[i], days[i]) for i in range(len(data))]
    days = [(dates[i] - day0).days for i in range(len(data))]
    
    # apply filter
    deathsSmooth = np.convolve(deaths, binomcoeffs(nSmooth), mode='valid')
    datesSmooth = np.convolve(np.array(days), binomcoeffs(nSmooth), mode='valid')
    
    # Convert datesSmooth back to dates
    datesSmooth = [day0 + dt.timedelta(days=int(datesSmooth[i]))
         for i in range(len(datesSmooth))]
    
    return datesSmooth, deathsSmooth

def reproductiveRate(deaths):
    """
    For a smooth time series of deaths, return the reproductiveRate, r
    r is an array of size one less than deaths
    """
    r = 1e-6*np.ones(len(deaths)-1)
    for i in range(len(r)):
        if (deaths[i+1] > 0):
            r[i] = deaths[i]/deaths[i+1]
    
    return r

countries = ['United_Kingdom', 'Italy', 'China', 'United_States_of_America',
             'India', 'Brazil', 'Belgium']
continents = ['Europe', 'Europe', 'Asia', 'America', 'Asia', 'America', 'Europe']
colours = ['k', 'r', 'b', 'c', 'm', 'g', 'y']
nC = len(countries)

dates = [None] * nC;
deaths = [None] * nC;
r = [None] * nC;
nSmooth = 40

for ic in range(nC):
    [dates[ic], deaths[ic]] = \
         getSmoothData(continents[ic], countries[ic], nSmooth)
    r[ic] = reproductiveRate(deaths[ic])
    
    #Make deaths per 100 million population
    deaths[ic] *= 1e8

# Plot and save
plt.clf()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
for ic in range(nC):
    plt.plot(dates[ic], deaths[ic], colours[ic], label=countries[ic])
plt.legend()
plt.title("Deaths per day per 100 million population, binomial filtered")
plt.gcf().autofmt_xdate()
plt.savefig("output/countryDeaths.pdf")

# Plot the r values for each country as a function of time
plt.clf()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
for ic in range(nC):
    if ic != 2:
        plt.plot(dates[ic][1:], r[ic], colours[ic], label=countries[ic])
plt.legend()
plt.title("Reproductive rate")
plt.gcf().autofmt_xdate()
plt.ylim([0.8,1.4])
plt.axhline(y = 1, color='k', ls=':')
plt.savefig("output/reproductiveRate.pdf")

