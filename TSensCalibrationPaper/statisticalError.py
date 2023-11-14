import pandas as pd
import ROOT, os
from protoDUNEStyle import protoDUNEStyle
ROOT.gROOT.SetStyle("protoDUNEStyle")
ROOT.gROOT.ForceStyle()

pathToData = os.path.join(os.pardir, os.pardir, os.pardir, "RTDdata")
pathToSaveData = f"{pathToData}/ProcessedData/TGrad/"

LArresults = pd.read_csv(f"{pathToSaveData}LArTree.csv", header=0)
LArresults.columns = ["ID", "CC", "CC_err"]
LN22_results = pd.read_csv(f"{pathToSaveData}LN22Tree.csv", header=0)
LN22_results.columns = ["ID", "CC", "CC_err"]
LN23_results = pd.read_csv(f"{pathToSaveData}LN23Tree.csv", header=0)
LN23_results.columns = ["ID", "CC", "CC_err"]

def makeHistogram(dataFrame, saveFileName, title):
    canvas = ROOT.TCanvas("canvas", "Histogram Example", 800, 600)
    hist = ROOT.TH1F("myhist", f"{title}", 12, 0, 3.5)
    gaussian = ROOT.TF1("gaussian", "gaus", 0, 3.5)
    for index, row in dataFrame.iterrows():
        value = row["CC_err"]
        hist.Fill(value)
    hist.SetTitle("Statistical Errors Dsitribution")
    hist.GetXaxis().SetTitle("Statistical Error (mK)")
    hist.GetYaxis().SetTitle("# Counts")
    hist.SetLineColor(ROOT.kBlack)
    hist.Fit(gaussian, "R")
    hist.Draw("E")
    gaussian.Draw("same")
    canvas.Update()
    canvas.SaveAs(f"{pathToSaveData}/Plots/{saveFileName}.pdf")

makeHistogram(LArresults, "Lar2023", "Liquid Argon 2023")
makeHistogram(LN22_results, "LN22", "Liquid Nitrogen 2022")
makeHistogram(LN23_results, "LN23", "Liquid Nitrogen 2023")