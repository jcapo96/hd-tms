import pandas as pd
import ROOT, os
from protoDUNEStyle import protoDUNEStyle
ROOT.gROOT.SetStyle("protoDUNEStyle")
ROOT.gROOT.ForceStyle()

pathToData = os.path.join(os.pardir, os.pardir, os.pardir, "RTDdata")
pathToSaveData = f"{pathToData}/ProcessedData/TGrad/"

LArresults = pd.read_csv(f"{pathToSaveData}LArTree.csv", header=0)
LArresults.columns = ["ID", "CC", "CC_err"]
LAr2018results = pd.read_csv(f"{pathToSaveData}LAr2018.csv", header=0, sep=",")
LAr2018results["CC"] = LAr2018results["CC"]*1e3
LN22_results = pd.read_csv(f"{pathToSaveData}LN22Tree.csv", header=0)
LN22_results.columns = ["ID", "CC", "CC_err"]
LN23_results = pd.read_csv(f"{pathToSaveData}LN23Tree.csv", header=0)
LN23_results.columns = ["ID", "CC", "CC_err"]


calibrations = {
    "Lar2018":LAr2018results,
    "Lar2023":LArresults,
    "LN22":LN22_results,
    "LN23":LN23_results
}

def makeHistogram(cal1, cal2, ref, Lar2018Cal="CC", saveBool=True):
    if saveBool == True:
        canvas = ROOT.TCanvas("canvas", "Histogram Example", 800, 600)
        hist = ROOT.TH1F("myhist", f"{cal1}-{cal2}", 15, -15, 15)
        gaussian = ROOT.TF1("gaussian", "gaus", -15, 15)
    calibration1 = calibrations[cal1]
    calibration2 = calibrations[cal2]
    print(cal1, cal2)
    if cal1 == "Lar2018":
        calibration1[Lar2018Cal] = (calibration1[Lar2018Cal] - calibration1.loc[(calibration1["ID"]==ref)][Lar2018Cal].values[0])
    elif cal1 != "Lar2018":
        calibration1["CC"] = calibration1["CC"] - calibration1.loc[(calibration1["ID"]==ref)]["CC"].values[0]
    if cal2 == "Lar2018":
        calibration2[Lar2018Cal] = (calibration2[Lar2018Cal] - calibration2.loc[(calibration2["ID"]==ref)][Lar2018Cal].values[0])
    elif cal2 != "Lar2018":
        calibration2["CC"] = calibration2["CC"] - calibration2.loc[(calibration2["ID"]==ref)]["CC"].values[0]

    diffs= []
    for index, row in calibration1.iterrows():
        if cal1 == "Lar2018":
            value1 = row[Lar2018Cal]
        elif cal1 != "Lar2018":
            value1 = row["CC"]
        if cal2 == "Lar2018":
            row2 = calibration2.loc[(row["ID"]==calibration2["ID"])][Lar2018Cal]
        elif cal2 != "Lar2018":
            row2 = calibration2.loc[(row["ID"]==calibration2["ID"])]["CC"]
        if len(row2) == 0:
            continue
        value2 = row2.values[0]
        if saveBool == True:
            hist.Fill(value1-value2)
        diffs.append(value1-value2)
    
    if saveBool == True:
        hist.SetTitle(f"Calibration Constant Differences: {cal1}-{cal2}")
        hist.GetXaxis().SetTitle("Statistical Error (mK)")
        hist.GetYaxis().SetTitle("# Counts")
        hist.SetLineColor(ROOT.kBlack)
        hist.Fit(gaussian, "R")
        hist.Draw("E")
        sigma = gaussian.GetParameter(2)
        sigma_error = gaussian.GetParError(2)
        gaussian.Draw("same")
        canvas.Update()
        canvas.SaveAs(f"{pathToSaveData}/Plots/{cal1}-{cal2}.pdf")
    return diffs, sigma, sigma_error

# makeHistogram("LN22", "Lar2023", 40525, "CC")

def makeGraph(years=[2018, 2023.5, 2022.1, 2022.5]):
    canvas2 = ROOT.TCanvas("canvas2", "Graph Example", 800, 600)
    graph = ROOT.TGraphErrors()
    for index, key in enumerate(calibrations.keys()):
        diffs, sigma, sigma_error = makeHistogram("Lar2018", key, 40525, "CC", saveBool=True)
        if index == 0:
            graph.SetPoint(index, years[index], 3.0)
            graph.SetPointError(index, 0.2, 1.)
        elif index != 0:
            graph.SetPoint(index, years[index], sigma)
            graph.SetPointError(index, 0.2, sigma_error)
    graph.Draw("AP")
    graph.SetMarkerStyle(20)  # Marker style
    graph.SetMarkerSize(1.0)  # Marker size
    graph.SetMarkerColor(ROOT.kBlack)  # Marker color
    graph.SetTitle("Long-term offset Stability")
    graph.GetXaxis().SetTitle("Year")
    graph.GetYaxis().SetTitle("Standard Deviation [mK]")
    graph.GetYaxis().SetRangeUser(0, 6)
    # graph.GetXaxis().SetRangeUser(-1, 7)
    canvas2.Update()
    canvas2.SaveAs(f"{pathToSaveData}/Plots/standardDeviationYear.pdf")

makeGraph()

