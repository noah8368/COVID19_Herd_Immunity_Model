# Herd Immunity Prediction Model

###### Noah Himed
###### 13 March 2021

#### Summary

This repository contains a simplified model which attempts to take into account
several factors to generate a conservative prediction that serves as a
lower bound on how many days it will take a population reach herd immunity against
COVID19. This is a very simple simulation, and should not be used for any
serious purposes.

### Assumptions

The model makes the following assumptions

 1. The threshold for herd immunity for COVID19 is 75% [(source)](https://www.nytimes.com/2020/12/24/health/herd-immunity-covid-coronavirus.html)
 2. No additional infections of COVID19 will occur in the future
 3. Vaccinations will remain at a constant pace
 4. Vaccination and infection are statistically independent events

Assumptions (2) and (3) in particular allow this model to air on the side of
conservatism, as it is certain that additional COVID19 infections will occur
and almost certain that the rate of vaccination will increase as of the date
this document was written.

### Usage

The script `model.py` should be run from a POSIX shell in the following command:

    model.py [-h] [-p] POPULATION RECOVERED VACCINATED RATE

where `POPULATION` is the size of the studied population in millions,
`RECOVERED` is the size of the recovered population in millions, `VACCINATED`
is the size of the vaccinated population in millions, and `RATE` is the
rate at which new individuals are recieving at least one vaccine dose in
millions/day. The `-p` flag may be supplied to plot the portion of the population
which is immune over time.

The following are a set of good sources to find accurate, updated figures for
COVID19 statistics for the United States that may be used with this model:

 - [Estimated Total Infections (CDC)](https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/burden.html)
 - [COVID19 Vaccination Tracker (New York Times)](https://www.nytimes.com/interactive/2020/us/covid-19-vaccine-doses.html)
