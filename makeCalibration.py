from ROOTconverter.calibrationMethods import RefMethod, TreeMethod
import pandas as pd
import json, os

pathToData = os.path.join(os.pardir, os.pardir, os.pardir, "RTDdata")
pathToSaveData = f"{pathToData}/ProcessedData/TGrad/"

file = open("keys/calibrationRunsInfo.json")
calibration_runs = json.load(file)
LArTgrad = TreeMethod(
            calibration_runs["LAr_2023"],
            calibration_runs["raised_sensors"]
)

LN2Tgrad_2022 = TreeMethod(
            calibration_runs["LN2_2022"],
            calibration_runs["raised_sensors"]
)

LN2Tgrad_2023 = TreeMethod(
            calibration_runs["LN2_2023"],
            calibration_runs["raised_sensors"]
)

LArresults = pd.DataFrame.from_dict(LArTgrad.get_calresults(bestpathBool=True)).T
LArresults.columns = ["CC", "CC_err"]
LArresults.to_csv(f"{pathToSaveData}LArTree.csv", index=True)


LN22_results = pd.DataFrame.from_dict(LN2Tgrad_2022.get_calresults(bestpathBool=True)).T
LN22_results.columns = ["CC", "CC_err"]
LN22_results.to_csv(f"{pathToSaveData}LN22Tree.csv", index=True)


LN23_results = pd.DataFrame.from_dict(LN2Tgrad_2023.get_calresults(bestpathBool=True)).T
LN23_results.columns = ["CC", "CC_err"]
LN23_results.to_csv(f"{pathToSaveData}LN23Tree.csv", index=True)

