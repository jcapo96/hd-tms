import pandas as pd
import numpy as np
import glob, os
import datetime

#This function considers the format of the timestamp and transofrms it to LINUX epoch time. There are tow types of timestamps among the data files: one containing AM/PM notation and the other one ranging from 0-24h. The function is able to manage both types and correctly convert them to epoch time in seconds.
def time_to_seconds(timestamp):
    date, time = timestamp.split("-")
    day, month, year = [int(x) for x in date.split("/")]
    h, m, s = [x for x in time.split(":")]
    h, m = int(h), int(m)
    try:
        s, pmam = [x for x in s.split(" ")]
        s = int(s)
        if pmam == "PM":
            if h == 12:
                h = h
            else:
                h = h + 12
        if pmam == "AM":
            if h == 12:
                h = h - 12
            else:
                h = h
        epoch = datetime.datetime(year, day, month, h, m, s).timestamp()
        return epoch
    except:
        s = int(s)
        epoch = datetime.datetime(year, month, day, h, m, s).timestamp()
        return epoch

#This function looks for the file in the folders, read the data for each selected file, converts the time to seconds frome epoch and converts the units to mK 
def read_datafile(row):
    path = os.path.join(os.pardir, os.pardir, os.pardir, "RTDdata")
    text_file = glob.glob(path + "/**/" + row["Filename"] + ".txt", recursive = True)
    path_to_file = text_file[0]
    # print("Path to file -------> " + path_to_file)
    data = pd.DataFrame(pd.read_csv(str(path_to_file), sep='\t', header=None))
    names = ["Date", "Time", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14"]
    data.columns = names
    data["Timestamp"] = (data["Date"] + "-" + data["Time"]).apply(time_to_seconds)
    del data["Date"]
    del data["Time"]
    return data

def get_sensors_id(row):
    sens_id = {}
    for i in range(1, 15):
        sens_id["s"+str(i)] = row["S"+str(i)]
    return sens_id

def compute_calibration_constant(data, ref):
    calconst = {}
    for sensor in data.columns:
        if sensor == "Timestamp" or sensor == "9999":
            continue
        calconst[sensor] = [1e3*np.mean(data[sensor]-data[ref]), 1e3*np.std(data[sensor]-data[ref])]
    return calconst

def swap_labels(sensor_id, calconst):
    swapped_calconst = {}
    for channel, sensor in sensor_id.items():
        if sensor == "44123" or sensor == "44124":
            continue
        swapped_calconst[sensor] = calconst[channel]
    return swapped_calconst