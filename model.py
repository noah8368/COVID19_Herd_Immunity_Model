# Model the percentage of US population with some degree of COVID19 immunity

# Written 22 Jan 2021
# By Noah Himed

import argparse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

HERD_IMMUNITY_PERCENT = 0.75

# Define a class to model the population of the vaccinated and recovered population
class Model:
    def __init__(self, total_pop, recovered_pop, vax_pop, vax_rate):
        # Check that user-entered parameters are in valid ranges
        if total_pop < 0:
            raise ValueError("Total population must be positive")
        if recovered_pop < 0:
            raise ValueError("Recovered population must be positive")
        elif recovered_pop > total_pop:
            raise ValueError("Recovered population must be less than 330M")
        if vax_pop < 0:
            raise ValueError("Vaccinated population must be positive")
        elif vax_pop > total_pop:
            raise ValueError("Vaccinated population must be less than 330M")
        if vax_pop < 0:
            raise ValueError("Vaccination rate must be positive")
        elif vax_pop > total_pop:
            raise ValueError("Vaccination rate must be less than 330M/day")

        self.total_pop = total_pop
        self.vax_pop = vax_pop
        self.vax_rate = vax_rate
        self.recovered_pop = recovered_pop
        self.prob_recovered = recovered_pop/total_pop
        # Keep track of the portion of the US that has been infection/vaccinated
        initial_immune_pop = vax_pop * (1 - self.prob_recovered) + recovered_pop
        self.immune_pop_log = [initial_immune_pop/total_pop]

    def get_percent_immune(self):
        return self.immune_pop_log[-1]

    def get_sim_length(self):
        return len(self.immune_pop_log)

    def add_daily_vax(self):
        if (self.vax_pop + self.vax_rate <= self.total_pop):
            self.vax_pop += self.vax_rate
            # Subtract off vaccinated population that has recovered from COVID19
            only_vax_pop = self.vax_pop * (1 - self.prob_recovered)
            immune_pop = only_vax_pop + self.recovered_pop + self.immune_pop_log[-1]
            self.immune_pop_log.append(immune_pop/self.total_pop)

    def plot_immunity(self):
        # Create a list of date labels
        day_count = range(len(self.immune_pop_log))
        dates = []
        today = datetime.today()
        for count in day_count:
            day = today + timedelta(days=count)
            date = day.strftime("%d %b %Y")
            dates.append(date)

        fig, ax = plt.subplots()
        ax.plot_date(dates, self.immune_pop_log, color='g', linestyle='-',
                      label="Immune portion of population")
        ax.axhline(y=HERD_IMMUNITY_PERCENT, color='r', linestyle='-',
                    label="Herd Immunity Threshold")
        ax.set_title("Growth of COVID19 Immunity")
        ax.set_xlabel("Time")
        plt.xticks(rotation=60)
        spacing = 2
        for label in ax.xaxis.get_ticklabels()[::spacing]:
            label.set_visible(False)
        ax.set_ylabel("Percent of US Population")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("POPULATION", help="Size of studied population in \
                        millions",
                        type=float)
    parser.add_argument("RECOVERED", help="Number of recovered individuals in \
                        millions",
                        type=float)
    parser.add_argument("VACCINATED", help="Number of vaccinated individuals in \
                        millions",
                        type=float)
    parser.add_argument("RATE", help="Vaccination rate in millions/day", type=float)
    parser.add_argument("-p", "--plot",
                        help="Plot the portion of immune people in the simulation",
                        action="store_true")
    args = parser.parse_args()

    model = Model(args.POPULATION, args.RECOVERED, args.VACCINATED, args.RATE)

    # Add vaccinations until the herd immunity threshold has been reached
    percent_immune = model.get_percent_immune()
    while percent_immune < HERD_IMMUNITY_PERCENT:
        model.add_daily_vax()
        percent_immune = model.get_percent_immune()
    prediction = model.get_sim_length()

    print("Prediction: ", str(prediction), "days")
    if (args.plot):
        model.plot_immunity()
