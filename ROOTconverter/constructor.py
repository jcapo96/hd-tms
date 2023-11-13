import numpy as np
import pandas as pd
import copy
import ROOTconverter.file_manager, ROOTconverter.data_manager
import matplotlib.pyplot as plt

log_file = ROOTconverter.file_manager.download_logfile()

class CalibrationSet():
    def __init__(self, ref, kwargs):
        self.logfile = log_file
        self.data_path ="/Users/jcapo/Documents/Software/TMS/RTDdata/Data"
        self.ref = ref
        self.conditions = kwargs #A dict containing conditions to filter the logfile and obtain the selection
        self.selection = None #Stores the selection of the data files as a DataFrame
        self.data = {}  # Stores the calibration data as a DataFrame
        self.mean = {}
        self.calconst = {}
        self.sensor_ids = {}
    
    def select_files(self):
        self.selection = log_file.copy()
        for i, j in self.conditions.items():
            self.selection = self.selection.loc[(self.selection[i]==j)]
        return self.selection

    def get_description(self):
        selection = self.select_files()
        self.sensor_ids = {}
        for index, row in selection.iterrows():
            self.sensor_ids[row["N_Run"]] = ROOTconverter.data_manager.get_sensors_id(row)

        first_dict = self.sensor_ids[row["N_Run"]]
        all_equal = all(first_dict == copy.deepcopy(sensor_ids) for sensor_ids in self.sensor_ids.values())

        if all_equal:
            self.sensor_ids = first_dict
            return self.sensor_ids  # Return the first dictionary
        else:
            self.sensor_ids = first_dict
            return self.sensor_ids
        
    def get_data(self):
        selection = self.select_files()
        for index, row in selection.iterrows():
            self.data[row["N_Run"]] = ROOTconverter.data_manager.read_datafile(row)
            names = (list((self.get_description().values())))
            names.append("Timestamp")
            self.data[row["N_Run"]].columns = names
        return self.data

    def get_means(self):
        data = self.get_data()
        for run in data.keys():
            t0 = min(data[run]["Timestamp"])
            data[run] = data[run].loc[(data[run]["Timestamp"]-t0>1000) & (data[run]["Timestamp"]-t0<2000)]
            self.mean[run] = ROOTconverter.data_manager.compute_calibration_constant(data[run], ref=self.ref)
        return self.mean
    
    def get_calibration_constants(self):
        means = self.get_means()
        for run, run_data in means.items():
            for sensor, sensor_data in run_data.items():
                if sensor not in self.calconst:
                    self.calconst[sensor] = []
                self.calconst[sensor].append(sensor_data[0])
        for sensor, sensor_data in self.calconst.items():
            self.calconst[sensor] = [np.mean(sensor_data), np.std(sensor_data)]
        #self.calconst = data_manager.swap_labels(self.get_description(), self.calconst)
        return self.calconst