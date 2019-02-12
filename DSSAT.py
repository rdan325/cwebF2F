'''
Module for wrapping the DSSAT model with Python
Formerly "InputCreator"
'''

import os
import csv
import sys
import numpy as np
import pandas as pd
import datetime as dt
from numpy import mean


class DSSATFile:

    def __init__(self, crop, cultivar, soil, weather, st_yr, p_mo, p_day, ppop, h_mo, h_day, wsuff, irrsim='A'):

        # Parse variables from json object
        self.crop = crop
        self.cultivar = cultivar
        self.soil = soil
        self.weather = weather
        self.st_yr = st_yr
        self.p_mo = p_mo
        self.p_day = p_day
        self.ppop = ppop
        self.pmeth = 'S'
        self.row_space = 75
        self.pdepth = 5
        self.mode = 'B'
        self.h_mo = h_mo
        self.h_day = h_day
        self.w_suff = wsuff
        self.irrsim = irrsim

    def Batch(self):

            """
                This function is used to write the batch file.
                All modes except for batch mode were taken out as this mode is only
                used for individual treatments
                Writes experiment file with format LLLLYYYY.WTH: L = location, Y = year
            """
            batchfile = open(os.path.join('\\DSSAT46', 'run.v46'), 'w')
# Change .BTX file to .MZX, .SBX, or .WHX
            if self.crop == "Maize":
                batchfile.write("$BATCH(BATCH)\n!\n")
                batchfile.write(
                        "@FILEX                                                                                        TRTNO     RP     SQ     OP     CO\n")
                batchfile.write(
                        "%s%4d.MZX                                                                                     %d       %d      %d      %d      %d" % (
                                self.weather, self.st_yr, 1, 1, 0, 0, 0))
            elif self.crop == "Soybean":
                batchfile.write("$BATCH(BATCH)\n!\n")
                batchfile.write(
                        "@FILEX                                                                                        TRTNO     RP     SQ     OP     CO\n")
                batchfile.write(
                        "%s%4d.SBX                                                                                     %d       %d      %d      %d      %d" % (
                                self.weather, self.st_yr, 1, 1, 0, 0, 0))
            elif self.crop == "Wheat":
                batchfile.write("$BATCH(BATCH)\n!\n")
                batchfile.write(
                        "@FILEX                                                                                        TRTNO     RP     SQ     OP     CO\n")
                batchfile.write(
                        "%s%4d.WHX                                                                                     %d       %d      %d      %d      %d" % (
                                self.weather, self.st_yr, 1, 1, 0, 0, 0))
# Removed debug mode option
            batchfile.close()
            return

    def Control(self):

            """
               This function is used to write the experiment file.
               Writes experiment file with format LLLLYYYY.WTH: L = location, Y = year
            """
            path = ".//DSSAT46"

            if self.crop == "Maize":
                file = open(os.path.join('%s'%(path), "%s%4d.MZX"%(self.weather, self.st_yr)), "w")
            elif self.crop == "Soybean":
                file = open(os.path.join('%s'%(path), "%s%4d.SBX"%(self.weather, self.st_yr)), "w")
            elif self.crop == "Wheat":
                file = open(os.path.join('%s'%(path), "%s%4d.WHX"%(self.weather, self.st_yr)), "w")
            else:
                file = None
# Removed debug mode

            file.write("*EXP.DETAILS: %s%s%s\n" % (self.weather, self.wmodel,str(self.game)))
            file.write("\n*GENERAL\n@PEOPLE\n-99\n@ADDRESS\n-99\n@SITE\n-99\n")
#                 file.write("    %d   %d   %d   %d   %d   %d   %d   %d   %d   %d\n" % (
#                         -99, -99, -99, -99, -99, -99, -99, -99, -99, -99))
            # Treatment
            try:
                i = pd.read_csv(os.path.join(path, 'IrrSched.csv'))
            except:
                i = pd.read_csv('IrrSched.csv')
            try:
                f = pd.read_csv(os.path.join(path, 'FertSched.csv'))
            except:
                f = pd.read_csv('FertSched.csv')
            try:
                r = pd.read_csv(os.path.join(path, 'OrgSched.csv'))
            except:
                r = pd.read_csv('OrgSched.csv')
            try:
                c = pd.read_csv(os.path.join(path, 'ChemSched.csv'))
            except:
                c = pd.read_csv('ChemSched.csv')
            try:
                t = pd.read_csv(os.path.join(path, 'TillSched.csv'))
            except:
                t = pd.read_csv('TillSched.csv')
            file.write("\n*TREATMENTS                        -------------FACTOR LEVELS------------\n")
            file.write("@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n")
            file.write("%2d %d %d %d %-25s%3s%3s%3s%3s%3s%3s%3s%3s%3s%3s%3s%3s%3s\n" %
                       (1, 1, 1, 0, "Sim", 1, 1, 0, 1, 1, int(r.empty == False), int(f.empty == False), int(r.empty == False),
                        int(c.empty == False), int(t.empty == False), 0, 1, 1))

            # Cultivar
            file.write("\n*CULTIVARS\n")
            file.write("@C CR INGENO CNAME\n")
            if self.crop == "Maize":
                if self.cultivar == 'short':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "990003", "SHORT SEASON"))
                elif self.cultivar == 'medium':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "990002", "MEDIUM SEASON"))
                elif self.cultivar == 'long':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "990001", "LONG SEASON"))
                elif self.cultivar == 'pioneer':
                    file.write("%2s %s %s %s %d\n" % (1, "MZ", "IB0012", "PIO", 3382))
                elif self.cultivar == 'GDD2700':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "PC0004", "2700-2750 GDD"))
                elif self.cultivar == 'GDD2650':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "PC0003", "2650-2700 GDD"))
                elif self.cultivar == 'GDD2600':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "PC0002", "2600-2650 GDD"))
                elif self.cultivar == 'GDD2500':
                    file.write("%2s %s %s %s\n" % (1, "MZ", "PC0001", "2500-2600 GDD"))
            elif self.crop == "Wheat":
                file.write("%2s %s %s %s\n" % (1, "WH", "IB0488", "NEWTON"))
            elif self.crop == "Soybean":
                file.write("%2s %s %s %s\n" % (1, "SB", "IB0011", "EVANS"))
            else:
                print("ERROR cultivar\n")

            # Locates .WTH file with format LLLLYYSS.WTH: L = location, Y = year, S = wsuff
            yr = str(self.st_yr)[2:]
            yr = yr + self.w_suff
            file.write("\n*FIELDS\n")
            file.write("@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\n")
            if self.soil == "Clay":
                file.write("%2s %s%4s %s%s   %d   %d   %s   %d   %d   %s  %d   %d  %s %d\n" % (
                    1, self.weather, "0001", self.weather, yr, -99, -99, -99, -99, -99, -99, -99, -99, "IB00000001",
                    -99))
            elif self.soil == "Loam":
                file.write("%2s %s%4s %s%s   %d   %d   %s   %d   %d   %s  %d   %d  %s %d\n" % (
                    1, self.weather, "0001", self.weather, yr, -99, -99, -99, -99, -99, -99, -99, -99, "IB00000004",
                    -99))
            elif self.soil == "Sand":
                file.write("%2s %s%4s %s%s   %d   %d   %s   %d   %d   %s  %d   %d  %s %d\n" % (
                    1, self.weather, "0001", self.weather, yr, -99, -99, -99, -99, -99, -99, -99, -99, "IB00000007",
                    -99))
            else:
                print("ERROR soil\n")
                exit()

            file.write("@L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR\n")
            file.write("%2s             %d             %d       %d               %d   %d   %d   %d   %d   %d\n" %
                       (1, -99, -99, -99, -99, -99, -99, -99, -99, -99))
            file.write("\n*INITIAL CONDITIONS\n")
            file.write("@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\n")
            date = dt.datetime(self.st_yr, 2, 1)  # Start simulation on February 1st
            doy = date.strftime("%y%j")
            file.write("%2s    %2s %5s   %d   %d     %d     %d   %d   %d   %d   %d   %d   %d %d\n" % (
                    1, "MZ", doy, 200, -99, 1, 1, -99, -99, -99, -99, -99, -99, -99))
# Soil layer parameters
            file.write("@C  ICBL  SH2O  SNH4  SNO3\n")
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 10, 0.21, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 20, 0.21, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 41, 0.24, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 71, 0.31, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 101, 0.32, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 126, 0.28, 0.1, 0.9))
            file.write("%2s  %3s  %.2f  %.1f  %.1f\n" % (1, 151, 0.28, 0.1, 0.9))
            # planting details
            file.write("\n*PLANTING DETAILS\n")
            file.write(
                    "@P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME\n")
            pdate = dt.datetime(self.st_yr, self.p_mo, self.p_day)
            pdoy = pdate.strftime("%y%j")
            file.write(
                "%2s %5s %5d  %4.1f  %4.1f %5s %5s %5d %5d %5d %5d %5d %5d %5d %3d                       %d\n" % (
                    1, pdoy, -99, self.ppop, self.ppop, self.pmeth, "R", self.row_space, 0, self.pdepth, -99, -99, -99, -99, -99, -99))

            # irrigation
            # doy(a,b) takes YEAR from IC and MONTH and DAY from MgtData and puts them into DSSAT compatible date
            def doy(a, b):
                return dt.datetime(self.st_yr, a, b).strftime("%y%j")

            try:
                file.write("\n*IRRIGATION AND WATER MANAGEMENT\n")
                file.write("@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n")
                file.write(
                        "%2s    %2s    %d    %d   %d %s %s    %d %d\n" % (1, 1, 30, 50, 100, "GS000", "IR001", 10, -99))
                file.write("@I IDATE  IROP IRVAL\n")
                i['DATE'] = i.apply(lambda row: doy(row['MONTH'],row['DAY']),axis=1)
                for idate in i.index:
                    file.write(
                        "%2s %5s %5s    %d\n" % (1, i['DATE'][idate], i['ROP'][idate], i['VAL'][idate]))
            except:
                file.write('\n')

            # fertilizers
            try:
                file.write("\n*FERTILIZERS (INORGANIC)\n")
                file.write("@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME\n")
                f['DATE'] = f.apply(lambda row: doy(row['MONTH'],row['DAY']),axis=1)
                for fdate in f.index:
                    file.write(
                        "%2s %5s %5s %5s %5d %5d %5d %5d %5d %5d %5d %3d\n" %
                        (1, f['DATE'][fdate], f['FMCD'][fdate], f['FACD'][fdate], f['FDEP'][fdate], f['FAMN'][fdate],
                         f['FAMP'][fdate], f['FAMK'][fdate], -99, -99, -99, -99))
            except:
                file.write('\n')

            # organic residue
            try:
                file.write("\n*RESIDUES AND ORGANIC FERTILIZER\n")
                file.write("@R RDATE  RCOD  RAMT  RESN  RESP  RESK  RINP  RDEP  RMET RENAME\n")
                r['DATE'] = r.apply(lambda row: doy(row['MONTH'],row['DAY']),axis=1)
                for rdate in r.index:
                    file.write(
                        "%2s %5s %5s %5d %5d %5d %5d %5d %5d %5s %3d\n"%(1,r['DATE'][rdate],r['RCOD'][rdate],r['RAMT'][rdate],r['RESN'][rdate],r['RESP'][rdate],r['RESK'][rdate],-99,-99,r['RMET'][rdate],-99))
            except:
                file.write('\n')
            # Chemical Applications

            try:
                file.write("\n*CHEMICAL APPLICATIONS\n")
                file.write("@C CDATE CHCOD CHAMT  CHME CHDEP   CHT..CHNAME\n")
                c['DATE'] = c.apply(lambda row: doy(row['MONTH'],row['DAY']),axis=1)
                for cdate in c.index:
                    file.write(
                        "%2s %5s %5s    %d %5s %d   %d  %d\n" % (1, c['DATE'][cdate], c['CHCOD'][cdate], c['CHAMT'][cdate], c['CHME'][cdate], c['CHDEP'][cdate], -99, -99))
            except:
                file.write('\n')

            # Tillage
            try:
                file.write("\n*TILLAGE AND ROTATIONS\n")
                file.write("@T TDATE TIMPL  TDEP TNAME\n")
                t['DATE'] = t.apply(lambda row: doy(row['MONTH'],row['DAY']),axis=1)
                file.write("%2s %5s %5s    %d  %d\n" % (1, t['DATE'][0],t['TIMPL'][0],t['TDEP'][0],t['TNAME'][0]))
            except:
                file.write('\n')

            # Harvest
            file.write("\n*HARVEST DETAILS\n")
            file.write("@H HDATE  HSTG  HCOM HSIZE   HPC  HBPC HNAME\n")
            hdoy = doy(self.h_mo,self.h_day)
            file.write("%2s %5s %5s     %s   %s   %s   %s %s\n" % (1, hdoy,"GS000","H",-99,-99,-99,self.crop))

            #Simulation controls
            file.write("\n*SIMULATION CONTROLS\n")
            file.write("@N GENERAL     NYERS NREPS START SDATE Ruser SNAME.................... SMODEL\n")
            sdoy = int(pdoy)-30 # Start simulation 30 days before planting date
            file.write("%2s %2s             %2s     %d     %s %5s  %d %s\n" % (1, "GE", 1, 1, "S", sdoy, 2150, "DEFAULT"))
            file.write("@N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2\n")
            file.write("%2s %2s              %s     %s     %s     %s     %s     %s     %s     %s     %s\n" % (1, "OP", "Y", "Y", "N", "N", "N", "N", "N", "Y", "D"))
# Does not yet simulate P or K
# Symbiosis not simulated
            file.write("@N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL\n")
            file.write("%2s %2s              %s     %s     %s     %s     %s     %s     %s     %d     %s     %s     %d\n" % (1, "ME", "M", "M", "E", "R", "S", "C", "R", 1, "G", "S", 2))
            file.write("@N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS\n")
            file.write("%2s %2s              %s     %s     %s     %s     %s\n" % (1, "MA", "R", self.irrsim, "R", "R", "R"))
            file.write("@N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT\n")
            file.write("%2s %2s              %s     %s     %s     %d     %s     %s     %s     %s     %s     %s     %s     %s     %s\n" % (1, "OU", "N", "Y", "Y", 1, "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"))

            #Automatic Management
            file.write('\n@  AUTOMATIC MANAGEMENT\n')
            file.write('@N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN\n')
            file.write(' 1 PL            001   001    40   100    30    40    10\n')
            file.write('@N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF\n')
            file.write(' 1 IR             30    75   100 GS000 IR004    10     1\n')
            file.write('@N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF\n')
            file.write(' 1 NI             30    50    25 FE001 GS000\n')
            file.write('@N RESIDUES    RIPCN RTIME RIDEP\n')
            file.write(' 1 RE            100     1    20\n')
            file.write('@N HARVEST     HFRST HLAST HPCNP HPCNR\n')
            file.write(' 1 HA              0   001   100     0\n')
            file.close()
            return

class Irrigation:
    """
    This class is for creating irrigation management data for a season
    """
    def __init__(self, yr, mo, d, method, amt):

        # Parse variables from json object
        self.yr = yr
        self.mo = mo
        self.d = d
        self.method = method
        self.amt = amt

        # Write data into .csv file
        path = '.\\DSSAT46\\IrrSched.csv'
        try:
            irr = pd.read_csv(path)
        except:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','ROP','VAL'])
            csvfile.close()
            irr = pd.read_csv(path)
        if irr.empty:
            with open(path,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','ROP','VAL'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.method), "%d" % (self.amt)))
        elif self.yr != irr['YEAR'].iloc[0]:
            with open(path,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','ROP','VAL'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.method), "%d" % (self.amt)))
        else:
            with open(path, 'a', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.method), "%d" % (self.amt)))
        csvfile.close()

class Fertilizer:
    """
    This class is for creating irrigation management data for a season
    """
    def __init__(self, yr, mo, d, fmat, fapp, fdep, famn, famp, famk):

        j = object
        self.yr = yr
        self.mo = mo
        self.d = d
        self.fmat = fmat
        self.fapp = fapp
        self.fdep = fdep
        self.famn = famn
        self.famp = famp
        self.famk = famk

        # Write data into .csv file
        path = '.\\DSSAT46\\FertSched.csv'
        try:
            fert = pd.read_csv(path)
        except:
            with open(path,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','FMCD','FACD','FDEP','FAMN','FAMP','FAMK'])
            csvfile.close()
            fert = pd.read_csv(path)
        if fert.empty:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','FMCD','FACD','FDEP','FAMN','FAMP','FAMK'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s"%(self.fmat), "%5s"%(self.fapp), "%d"%(self.fdep), "%d"%(self.famn), "%d"%(self.famp), "%d"%(self.famk)))
        elif self.yr != fert['YEAR'].iloc[0]:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','FMCD','FACD','FDEP','FAMN','FAMP','FAMK'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s"%(self.fmat), "%5s"%(self.fapp), "%d"%(self.fdep), "%d"%(self.famn), "%d"%(self.famp), "%d"%(self.famk)))
        else:
            with open(path, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s"%(self.fmat), "%5s"%(self.fapp), "%d"%(self.fdep), "%d"%(self.famn), "%d"%(self.famp), "%d"%(self.famk)))
        csvfile.close()

class Organic:
    """
    This class is for creating chemical management data for a season
    """
    def __init__(self, yr, mo, d, mat, amt, n, p, k, met):

        self.yr = yr
        self.mo = mo
        self.d = d
        self.mat = mat
        self.amt = amt
        self.n = n
        self.p = p
        self.k = k
        self.met = met

        # Write data into .csv file
        path = '.\\DSSAT46\\OrgSched.csv'
        res = pd.read_csv(path)
        if res.empty:
            with open(path,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','RCOD','RAMT','RESN','RESP','RESK','RMET'])
                writer.writerow(("%d" % (self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%d" % (self.n),"%d"%(self.p),"%d"%(self.k),"%5s"%(self.met)))

        elif self.yr != res['YEAR'].iloc[0]:
            with open(path,'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','RCOD','RAMT','RESN','RESP','RESK','RMET'])
                writer.writerow(("%d" % (self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%d" % (self.n),"%d"%(self.p),"%d"%(self.k),"%5s"%(self.met)))
        else:
            with open(path, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(("%d" % (self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%d" % (self.n),"%d"%(self.p),"%d"%(self.k),"%5s"%(self.met)))
        csvfile.close()

class Tillage:
    """
    This class is for specifying tillage management data for a season
    """
    def __init__(self, mo, d, imp, depth):

        self.mo = mo
        self.d = d
        self.imp = imp
        self.depth = depth

        # Write variables into .csv file
        path = '.\\DSSAT46\\TillSched.csv'
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
            writer.writerow(['MONTH','DAY','TIMPL','TDEP','TNAME'])
            writer.writerow(("%d" % (self.mo),"%d" % (self.d), "%5s" % (self.imp), "%d" % (self.depth), "-99"))
        csvfile.close()

class Chemicals:
    """
    This class is for specifying chemical management data for a season
    """
    def __init__(self, yr, mo, d, mat, amt, method, depth):

        self.yr = yr
        self.mo = mo
        self.d = d
        self.mat = mat
        self.amt = amt
        self.method = method
        self.depth = depth

        # Write data into .csv file
        path = '.\\DSSAT46\\ChemSched.csv'
        chem = pd.read_csv(path)
        if chem.empty:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','CHCOD','CHAMT','CHME','CHDEP','CHT','CHNAME'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%5s" % (self.method), "%d" % (self.depth)))
        elif self.yr != chem['YEAR'].iloc[0]:
            with open(path, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(['YEAR','MONTH','DAY','CHCOD','CHAMT','CHME','CHDEP','CHT','CHNAME'])
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%5s" % (self.method), "%d" % (self.depth)))
        else:
            with open(path, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
                writer.writerow(("%d"%(self.yr),"%d" % (self.mo),"%d" % (self.d), "%5s" % (self.mat), "%d" % (self.amt), "%5s" % (self.method), "%d" % (self.depth)))
        csvfile.close()


class DSSATModel(object):
    def __init__(self, ):
        self.mode = 'B'
        self.batchfile = 'run.v46'
        self.ofile = 'output.OUT'

    def Run(self):
        os.system('./dscsm047.exe %s %s > %s' % (self.mode, self.batchfile, self.ofile))
        file = open("Summary.OUT", 'r')
        r = file.readlines()[-1].split()
        file.close()
        y = int(r[21])
        i = int(r[30])
        return y, i


