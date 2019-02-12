from DSSAT import DSSATFile as DF
from DSSAT import DSSATModel as DM
from DSSAT import Irrigation, Fertilizer

'''
Module to optimize decision making in the corn and beef sectors
'''

class DssatOptimizer:
    def __init__(self, prices, wpath):
        self.prices = prices
        self.wpath = wpath  # path to weather directory

    def set_management(self):
        pass

    def run_dssat(self, crop, cultivar, soil, weather, st_yr, p_mo, p_day, ppop, h_mo, h_day, wsuff, nfert, irrsim='A'):
        Fertilizer(st_yr, p_mo, p_day, 'FE003', 'AP003', 5, nfert, 0, 0)
        file = DF(crop, cultivar, soil, weather, st_yr, p_mo, p_day, ppop, h_mo, h_day, wsuff, irrsim)
        file.Batch()
        file.Control()
        model = DM()
        model.Run()

    def dssat_test(self):
        cultivars = ['GDD2500', 'GDD2600', 'GDD2650', 'GDD2700']



class BcnrmOptimizer:
    def __init__(self, prices):
        self.prices = prices  # linear list of all prices in

    def set_ration(self):
        pass