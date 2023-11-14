import ROOT

# Create a TStyle object
protoDUNEStyle = ROOT.TStyle("protoDUNEStyle", "ProtoDUNE Style")

# Colors
protoDUNEStyle.SetFillColor(10)
protoDUNEStyle.SetFrameFillColor(10)
protoDUNEStyle.SetCanvasColor(10)
protoDUNEStyle.SetPadColor(10)
protoDUNEStyle.SetTitleFillColor(10)
protoDUNEStyle.SetStatColor(10)

protoDUNEStyle.SetFrameBorderMode(0)
protoDUNEStyle.SetCanvasBorderMode(0)
protoDUNEStyle.SetPadBorderMode(0)

protoDUNEStyle.SetPalette(1, 0)

protoDUNEStyle.SetHistLineColor(ROOT.kBlack)
protoDUNEStyle.SetFuncColor(ROOT.kRed)

protoDUNEStyle.SetLabelColor(ROOT.kBlack, "xyz")

protoDUNEStyle.SetTitleColor(ROOT.kBlack)

# Sizes
protoDUNEStyle.SetPadBottomMargin(0.125)
protoDUNEStyle.SetPadTopMargin(0.075)
protoDUNEStyle.SetPadLeftMargin(0.1)
protoDUNEStyle.SetPadRightMargin(0.1)

protoDUNEStyle.SetLabelSize(0.045, "xy")
protoDUNEStyle.SetLabelSize(0.035, "z")
protoDUNEStyle.SetLabelOffset(0.005, "xy")
protoDUNEStyle.SetTitleSize(0.05, "xyz")
protoDUNEStyle.SetTitleOffset(1, "x")
protoDUNEStyle.SetTitleOffset(1, "yz")
protoDUNEStyle.SetStatFontSize(0.05)
protoDUNEStyle.SetTextSize(0.05)
protoDUNEStyle.SetTitleBorderSize(0)
protoDUNEStyle.SetStatBorderSize(0)

protoDUNEStyle.SetHistLineWidth(3)
protoDUNEStyle.SetFrameLineWidth(2)
protoDUNEStyle.SetFuncWidth(2)

# Misc
protoDUNEStyle.SetNdivisions(506, "xy")

protoDUNEStyle.SetPadGridX(0)
protoDUNEStyle.SetPadGridY(0)

protoDUNEStyle.SetPadTickX(1)
protoDUNEStyle.SetPadTickY(1)

protoDUNEStyle.SetOptFit(1111)
protoDUNEStyle.SetOptStat(0)

protoDUNEStyle.SetMarkerStyle(20)
protoDUNEStyle.SetMarkerSize(0.9)

# Fonts
kProtoDUNEFont = 42
protoDUNEStyle.SetStatFont(kProtoDUNEFont)
protoDUNEStyle.SetLabelFont(kProtoDUNEFont, "xyz")
protoDUNEStyle.SetTitleFont(kProtoDUNEFont, "xyz")
protoDUNEStyle.SetTitleFont(kProtoDUNEFont, "")
protoDUNEStyle.SetTextFont(kProtoDUNEFont)

# Additional Customizations
protoDUNEStyle.SetCanvasBorderSize(0)
protoDUNEStyle.SetFrameBorderSize(0)
protoDUNEStyle.SetDrawBorder(0)
protoDUNEStyle.SetTitleBorderSize(0)

protoDUNEStyle.SetEndErrorSize(4)

protoDUNEStyle.SetStripDecimals(ROOT.kFALSE)

protoDUNEStyle.SetLegendBorderSize(0)
protoDUNEStyle.SetLegendFont(kProtoDUNEFont)

protoDUNEStyle.SetLabelOffset(0.015, "x")
protoDUNEStyle.SetLabelOffset(0.015, "y")
protoDUNEStyle.SetLabelOffset(0.01, "z")

protoDUNEStyle.SetTitleStyle(0)
protoDUNEStyle.SetTitleFont(kProtoDUNEFont, "pad")
protoDUNEStyle.SetTitleX(0.1)
protoDUNEStyle.SetTitleY(0.98)
protoDUNEStyle.SetTitleW(0.8)
protoDUNEStyle.SetLineStyleString(2, "[12 12]")

protoDUNEStyle.SetErrorX(0.001)

protoDUNEStyle.SetNumberContours(255)
protoDUNEStyle.SetPalette(ROOT.kBird)

# Apply the style
protoDUNEStyle.cd()
ROOT.gROOT.ForceStyle()
ROOT.gStyle.ls()

# Set the maximum number of digits in axis labels
ROOT.TGaxis.SetMaxDigits(4)
