import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pathToData = os.path.join(os.pardir, os.pardir, os.pardir, "RTDdata")
pathToSaveData = f"{pathToData}/ProcessedData/IFIC_Readout_Calib/"

results, resultsErr, channels = [], [], []
for channelNumber in range(2, 13):
    fileName1 = f"{pathToData}/Data/IFIC_Readout_Calib/20231114_CH1HP1_CH{channelNumber}_HP2.txt"
    fileName2 = f"{pathToData}/Data/IFIC_Readout_Calib/20231114_CH1HP2_CH{channelNumber}_HP1.txt"
    data1 = pd.read_csv(fileName1, sep="\t", header=None)
    data2 = pd.read_csv(fileName2, sep="\t", header=None)

    value1 = (data1[2] - data1[1+channelNumber]).mean()*1e3
    value1Err = (data1[2] - data1[1+channelNumber]).std()*1e3
    value2 = -(data2[2] - data2[1+channelNumber]).mean()*1e3
    value2Err = -(data2[2] - data2[1+channelNumber]).std()*1e3

    results.append(value1 - value2)
    resultsErr.append(np.sqrt(value1Err**2 + value2Err**2))
    channels.append(channelNumber+6)

plt.errorbar(channels, results, yerr= resultsErr, fmt="o", capsize=10, label=fr"$\mu$=3.6 mK; $\sigma$=0.56 mK")
plt.xlabel("Channel Number")
plt.ylabel("Readout Calibration Constant (mK)")
plt.title("IFIC Readout Calibration")
plt.grid("on")
plt.legend()
plt.savefig(f"{pathToSaveData}Plots/IFIC_Readout_Calib.pdf", format="pdf")
plt.show(block=True)
    
    