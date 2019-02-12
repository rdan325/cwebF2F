import pandas as pd
import datetime.datetime as dt
import shutil
import os

'''
Module for wrapping BCNRM software with Python
'''

class BCNRM:
    def __init__(self, weather, yr, mo, d, age, sex, breed1, breed2, clim, wpath="..//weather-repo"):
        self.wpath = wpath
        self.weather = weather
        self.yr = yr
        self.mo = mo
        self.d = d
        self.age = age
        self.sex = sex
        self.breed1 = breed1
        self.breed2 = breed2
        self.clim = clim

    def beef_fast_high(self):
        '''
        The inputs described are for:
            adg = 3.02
            corn = 11.7
            dgs = 4.5
            hay = 1.8
            breed = 1
        Need to change for each different t_lookup.csv files and different inputs
        '''


        temps = pd.read_csv('t_lookup_high.csv')
        doy = dt(self.yr, self.mo, self.d).strftime("%y%j")
        day = dt(self.yr, self.mo, self.d).strftime("%j")
        yrchar = doy[:2]
        wthname = self.weather + yrchar + self.clim + '5'

        path = os.path.join(self.wpath, 'RCP%s_5/%s.WTH' % (self.clim, wthname))
        shutil.copy(path, '.')
        file = open("%s.WTH" % (wthname))
        wth = file.readlines()[3:-1]
        file.close()
        wth = [x.split() for x in wth]
        df = pd.DataFrame(wth)
        df.columns = df.iloc[0]
        df = df.drop(0)
        df['TMIN'] = [float(x) for x in df['TMIN']]
        df['TMAX'] = [float(x) for x in df['TMAX']]
        df['TAVE'] = (df['TMIN'] + df['TMAX']) / 2
        df['MONTH'] = [dt.strptime(x, '%y%j').strftime('%m/%d/%y')[:2] for x in df['@DATE']]
        weather = df.groupby(['MONTH'])
        wave = weather['TAVE'].agg(['mean', 'count'])
        start = int(day)
        day = int(day)
        month = self.mo

        gain = 3.02
        methane = 109.267
        excreteN = 67.3
        corn_total = 0
        dgs_total = 0
        drink = 0
        gain_total = 0
        excreteN_total = 0
        methane_total = 0
        w = 900

        while w < 1250:
            t = wave.loc["%02d" % (month), 'mean']
            t = round(t)
            days = wave.loc["%02d" % (month), 'count']
            drink += float(temps.loc[temps['temp'] == t, 'water'])
            w += gain * days
            corn_total += 11.7 * days
            dgs_total += 4.5 * days
            gain_total += gain * days
            excreteN_total += excreteN * days
            methane_total += methane * days
            month += 1
            print("Weight is %f; Month is %d" % (w, month))
        finishing_time = month - self.mo
        os.remove('%s.WTH' % (wthname))

        out = {'Total Gain': gain_total, 'Total Corn': corn_total, 'Total DGS': dgs_total,
               'Finishing Time': finishing_time, 'Total Methane': methane_total, 'Total N': excreteN_total,
               'Water Drank': drink}
        return out
