# Written 22 Jan 2021
# By Noah Himed

import matplotlib.pyplot as plt
import datetime as dt

# https://www.worldometers.info/world-population/us-population/#:~:text=the%20United%20States%202020%20population,(and%20dependencies)%20by%20population.
US_POP = 332110000.0
# https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/burden.html
RECOVERED_POP = 83100000.0
# https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article?deliveryName=USCDC_333-DM25287
ORIG_R0 = 5.7
# https://www.nytimes.com/2020/12/31/health/coronavirus-variant-transmission.html
NEW_VARIANT_TRANSMISSION_BOOST = 1.56
# https://ourworldindata.org/covid-vaccinations
VACCINATED_POPULATION = 17550000.0
# https://covidtracking.com/data/charts/us-daily-positive
CASES_PER_DAY = 184864.0
# https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2768834?guestAccessKey=7a5c32e6-3c27-41b3-b46c-43c4a38bbe00&utm_source=For_The_Media&utm_medium=referral&utm_campaign=ftm_links&utm_content=tfl&utm_term=072120
# since testing has increased in capacity, number of unreported cases will be
# estimated to be half that of what it was in March-May. A conservative estimate
# for this latter figure is 5/6, so we'll use 5/12.
PERCENT_UNREPORTED_CASES = 5.0/12.0
# https://www.statnews.com/2020/12/19/a-side-by-side-comparison-of-the-pfizer-biontech-and-moderna-vaccines/
PFIZER_EFFICACY = 0.95
MODERNA_EFFICACY = 0.9425
# https://ourworldindata.org/covid-vaccinations
DAILY_VAC_RATE = 1000000
# ngl kinda just pulled these outta my ass
REINFECTION_RATE = 0.05
DAILY_VAX_INCREASE = 10000
MAX_VAX_CAPACITY = 3000000

VAX_RECORD = []
INFECTION_RECORD = []
HERD_RECORD = []

def herd_immunity_pop(r0):
  return US_POP*(1 - (1/r0))

R0 = ORIG_R0*NEW_VARIANT_TRANSMISSION_BOOST
HERD_IMMUNITY_THRESHOLD = herd_immunity_pop(R0)

def vax_rate(t):
  return min(DAILY_VAC_RATE + DAILY_VAX_INCREASE*t, MAX_VAX_CAPACITY)

def vaccine_protected_pop(t, efficacy):
  daily_vax = vax_rate(t)
  global VACCINATED_POPULATION
  VACCINATED_POPULATION += daily_vax
  return efficacy*(VACCINATED_POPULATION)

def infection_protected_pop(t, infection_rate, reinfection_prob):
  return (1-reinfection_prob)*(infection_rate*t + RECOVERED_POP)

def vaccinated_infected_pop(vac_pop, recovered_pop):
  return (vac_pop*recovered_pop)/US_POP

def people_left(t, r0, avg_cases_until_end, vaccine_efficacy):
  inf_pop = infection_protected_pop(t, avg_cases_until_end, REINFECTION_RATE)
  global INFECTION_RECORD
  INFECTION_RECORD.append(inf_pop)
  vax_pop = vaccine_protected_pop(t, vaccine_efficacy)
  global VAX_RECORD
  VAX_RECORD.append(vax_pop)
  inf_vax_overlap = vaccinated_infected_pop(vax_pop, inf_pop)
  global HERD_IMMUNITY_THRESHOLD
  herd_size = HERD_IMMUNITY_THRESHOLD - vax_pop - inf_pop + inf_vax_overlap
  HERD_RECORD.append(herd_size)
  return herd_size

vaccine_efficacy = (PFIZER_EFFICACY + MODERNA_EFFICACY)/2
avg_cases_until_end = (CASES_PER_DAY*(1 + PERCENT_UNREPORTED_CASES))/2

days_from_now = 0

herd_pop = people_left(days_from_now, R0, avg_cases_until_end, vaccine_efficacy)
while herd_pop > 0:
  days_from_now += 1
  herd_pop = people_left(days_from_now, R0, avg_cases_until_end, vaccine_efficacy)

time = range(days_from_now+1)
plt.plot(time, VAX_RECORD, color="green", label="Protected by Vaccination")
plt.plot(time, INFECTION_RECORD, color="red", label="Protected by Infection")
plt.plot(time, HERD_RECORD, color="blue", label="People Left to Protect")
plt.xlabel("Days From Today")
plt.ylabel("People in 100s of Millions")
plt.title("Immunized Population Growth in US")
plt.legend()
plt.show()

print("Prediction: The US will reach herd immunity", str(days_from_now), "days from today on", str(dt.date.today() + dt.timedelta(days=days_from_now)))
print("This model assumes an r_0 of", str(round(R0, 2)), "in a world without any restritions, requiring ~"+str(int(HERD_IMMUNITY_THRESHOLD)),
      "people to become immunized through infection or vaccination.")
print("This model uses the the current vaccination rate of ~"+str(DAILY_VAC_RATE), "people/day and a projected linear increase in this number by", DAILY_VAX_INCREASE,
      "additional people per day\nin addition to a calculated average of ~"+str(round(CASES_PER_DAY)), "infections per day through the end of the pandemic.")
print("The model also assumes a maximum vaccination capacity of ~"+str(MAX_VAX_CAPACITY), "people/day. These predictions are very informal and should be taken with a grain of salt.")
