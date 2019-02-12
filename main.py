import pandas as pd

from random import randint
from random import uniform
import numpy as np

from DSSAT import DSSATFile as DF
from DSSAT import DSSATModel as DM
from BCNRM import BCNRM
from GREET import GREET
from GroundWater import GroundWater as GW
from DecisionOptimizer import DssatOptimizer as DO
from DecisionOptimizer import BcnrmOptimizer as BO


class Main:
    def __init__(self, wpath="..//weather-repo"):
        self.wpath = wpath  # path to weather directory to copy from

    def main(self):
        yrs = range(2020, 2051)
        for y in yrs:
            prices = pd.read_csv("prices.csv")
            while True:
                try:
                    feedlot_id = self.pick_random_field("feedlot")
                    dgs_price = self.set_dgs_price(feedlot_id)
                    prices.loc['DGS', -1] = dgs_price  # set DGS price of latest year in prices data
                    year_prices = prices.iloc[-1].values
                    BO(year_prices).set_ration()  # updates feedlot record with optimal feed based on economics
                # if there are no fields left, it will trigger an exception and move on
                except ValueError:
                    break

            # perform same loop for all crop fields
            year_prices = prices.iloc[-1].values
            crop_data = pd.read_csv("crop_input.csv")
            while True:
                try:
                    crop_id = self.pick_random_field("crop")

                    if y == yrs[0]:
                        break
                    else:  # TODO create GroundWater functions
                        GW().set_soil_moisture()
                        GW().set_water_table()

                    DO(year_prices, self.wpath).set_management()  # updates crop management optimally based on economics
                    # TODO run DSSAT with management inputs ran from DO(year_prices, wpath)
                    lat = crop_data['lat'].where(crop_data['crop_id'] == crop_id)
                    long = crop_data['long'].where(crop_data['crop_id'] == crop_id)
                    yld = crop_data['yield'].where(crop_data['crop_id'] == crop_id)
                    dump_type, dump_id, dist = self.nearest_dump(lat, long)

                    data = {'crop_id': crop_id, 'dump_id': dump_id, 'dump_type': dump_type, 'year': y, 'distance': dist}

                    greet = GREET(dump_type, yld, dist)
                    greet_data = greet.model()
                    data['amount'] = greet_data['amount']
                    data['fossil_fuel'] = greet_data['ff']
                    data['ghg'] = greet_data['ghg']
                    data['water'] = greet_data['water']

                    df = pd.DataFrame(data)
                    with open("transactions.csv", "a") as csvfile:
                        df.to_csv(csvfile, header=False)
                except ValueError:
                    break

    def pick_random_field(self, operation):
        fields = pd.DataFrame()
        if operation == "crop":
            fields = pd.read_csv("crop_input.csv")
            fields = fields[fields['yield'] == 0]
        elif operation == "feedlot":
            fields = pd.read_csv("feedlot_input.csv")
            fields = fields[fields['corn_filled'] == 0]
        elif operation == "grass":
            fields = pd.read_csv("grass_input.csv")
        total = len(fields)
        return randint(1, total)

    def set_prices(self):
        pass

    def set_dgs_price(self, feedlot_id):
        return uniform(0, 1)

    def nearest_dump(self, lat, long):
        dump_type = "ethanol"
        dump_id = 1
        distance = 101.1
        return dump_type, dump_id, distance


