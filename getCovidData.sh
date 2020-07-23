#!/bin/bash -e
#

wget https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
mv csv covidData.csv

# First sort out Bonaire
sed -i 's/\"Bonaire\,\ Saint\ Eustatius\ and\ Saba\"/Bonaire_Saint_Eustatius_and_Saba/g' covidData.csv

continents=`awk -F',' '{if(NR>1) print $11}' covidData.csv | sort -u`
mkdir -p continents
for cont in $continents; do
    mkdir -p continents/$cont
    countries=`grep $cont covidData.csv | awk -F',' '{print $7}'  | sort -u`
    for c in $countries; do
        head -1 covidData.csv | awk -F',' '{print "#" $1, $2, $3, $4, $5, $6, $10, $12}' \
             > continents/$cont/$c.dat
        grep $c covidData.csv | awk -F',' '{print $1, $2, $3, $4, $5, $6, $10, $12+0}' \
            >> continents/$cont/$c.dat
    done
done

