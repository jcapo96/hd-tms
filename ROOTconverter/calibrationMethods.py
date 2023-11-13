from ROOTconverter.constructor import CalibrationSet
import numpy as np

class RefMethod():
    def __init__(self, selection):
        self.ref1 = "44123"
        self.ref2 = "44124"
        self.selection = selection
        self.calibsetnumbers = [calset["CalibSetNumber"] for calset in self.selection]
        self.calresults = {}
    
    def get_calresults(self):
        all_cal_results = {}
        for i, ref in enumerate([self.ref1, self.ref2]):
            all_cal_results[ref] = {}
            for calset, calibsetnumber in enumerate(self.calibsetnumbers):
                if "2.1" in calibsetnumber:
                    continue
                calset = CalibrationSet(ref=ref, kwargs=self.selection[calset])
                calconst = calset.get_calibration_constants()
                all_cal_results[ref].update(calconst)

        self.calresults = all_cal_results
        return self.calresults


class TreeMethod():
    def __init__(self, selection, raised):
        self.ref = "40525"
        self.selection = selection
        self.calibsetnumbers = [calset["CalibSetNumber"] for calset in self.selection]
        self.calresults = {}
        self.raised = raised

    def find_best_path(self, set):
        calconst_path = {}
        for i, auxref in enumerate(self.raised[set]):
            root_calset = CalibrationSet(ref=auxref, kwargs=self.selection[int(set)-1])
            top_calset = CalibrationSet(ref=self.ref, kwargs=self.selection[4])

            root_cc = root_calset.get_calibration_constants()
            top_cc = top_calset.get_calibration_constants()

            calconst = {}
            for sensor, values in root_cc.items():
                if sensor == "44123" or sensor == "44124":
                    continue
                cc = values[0] + top_cc[auxref][0]
                cc_err = np.sqrt(values[1]**2 + top_cc[auxref][1]**2)
                calconst[sensor] = [cc, cc_err]
            calconst_path[auxref] = calconst
        
        best_path = ""
        best_mean, best_sigma = 1e9, 1e9
        container = []
        for auxref in calconst_path.keys():
            for sensor in calconst_path[auxref].keys():
                container.append(calconst_path[auxref][sensor][1])
            if np.mean(container) < best_mean:
                # print(auxref, best_mean, np.mean(container))
                best_mean = np.mean(container)
                best_path = auxref
        return calconst_path, best_path
    
    def get_calresults(self, bestpathBool=False):
        all_cal_results = {}
        for calset, calibsetnumber in enumerate(self.calibsetnumbers):
            if "2.1" in calibsetnumber:
                continue
            calconst_path, best_path = self.find_best_path(calibsetnumber[-1])
            print(best_path)
            # print(calconst_path)
            if bestpathBool == True:
                if "1" in calibsetnumber:
                    best_path = "40525"
                if "2" in calibsetnumber:
                    best_path = "39647"
                if "3" in calibsetnumber:
                    best_path = "39613"
                if "4" in calibsetnumber:
                    best_path = "39666"
            #print(calibsetnumber, best_path)
            all_cal_results.update(calconst_path[best_path])
        self.calresults = all_cal_results
        return self.calresults