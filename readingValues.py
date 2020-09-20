# Reading script
import csv
import matplotlib.pyplot as plt
import statistics as st
import scipy.stats as stats
import numpy as np

def makeGrpahics(ax, control, avp, labels, mark):
    criterions  = ["0.2000", "0.4285", "0.6000", "0.8000", "0.9000"]
    probs = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]
    listControl = []
    semsControl = []
    for prob, values in control.items():
        listControl.append(st.mean(values))
        semsControl.append(stats.sem(values))
    listAVP = []
    semsAVP = []
    for prob, values in avp.items():
        listAVP.append(st.mean(values))
        semsAVP.append(stats.sem(values))

    dataControl = np.array(listControl)
    dataAVP = np.array(listAVP)

    stat, p = stats.shapiro(dataControl)
    if p > 0.05:
        pass#print('Control looks Gaussian (fail to reject H0)')
    else:
    	pass#print('Control does not look Gaussian (reject H0)')
    stat, p = stats.shapiro(dataAVP)
    if p > 0.05:
        pass#print('AVP looks Gaussian (fail to reject H0)')
    else:
    	pass#print('AVP does not look Gaussian (reject H0)')

    diffs = []
    for prob in criterions:
        samp1 = control[prob]
        samp2 = avp[prob]
        stat, p = stats.ttest_ind(samp1, samp2)
        diffs.append(p)

    ax.errorbar(probs, dataControl, yerr=semsControl, marker=mark, c='#0000FF', alpha=1, label=labels[0])
    ax.errorbar(probs, dataAVP, yerr=semsAVP, marker=mark, c='#FF0000', alpha=1, label=labels[1])
    for i, tag in enumerate(range(len(dataControl))):
        ax.annotate("{:.4f}".format(diffs[i]), (probs[i], dataControl[i]))
    ax.legend()

def darkGraph():
    plt.rcParams.update({                   # Plot style configuration
        "lines.color": "white",
        "patch.edgecolor": "white",
        "text.color": "white",
        "axes.facecolor": "black",
        "axes.edgecolor": "lightgray",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "grid.color": "lightgray",
        "figure.facecolor": "black",
        "figure.edgecolor": "black",
        "savefig.facecolor": "black",
        "savefig.edgecolor": "black"})

def generateGraph(animals, sliceNum, sliceSide, sections, fixedRadius, criterias, criterions):

    ccC = {}
    isC = {}
    gcC = {}
    trC = {}
    ccA = {}
    isA = {}
    gcA = {}
    trA = {}

    NullccC = {}
    NullisC = {}
    NullgcC = {}
    NulltrC = {}
    NullccA = {}
    NullisA = {}
    NullgcA = {}
    NulltrA = {}

    for criterion in criterions:
        ccRecC = []
        isRecC = []
        gcRecC = []
        trRecC = []
        ccRecA = []
        isRecA = []
        gcRecA = []
        trRecA = []

        NullccRecC = []
        NullisRecC = []
        NullgcRecC = []
        NulltrRecC = []
        NullccRecA = []
        NullisRecA = []
        NullgcRecA = []
        NulltrRecA = []
        for sliceN in sliceNum:
            for sliceS in sliceSide:
                for section in sections:
                    for fRad in fixedRadius:
                        for criteria in criterias:
                            for animal in animals:
                                fileType = "GT"
                                folderPath = "savedData/" + animal + "/Criteria " + criteria + "/" + criterion + "/" + sliceN + sliceS + "/" + section + "/"
                                fileName = animal + " - " + fileType + ".csv"
                                location = folderPath + fileName
                                an = animal.split()
                                with open(location) as file:        # Open the file at given location
                                    reader = csv.DictReader(file)
                                    for row in reader:              # Reads out each fow
                                        if an[0] == "Control":
                                            ccRecC.append(int(row["connected components"]))
                                            isRecC.append(int(row["isolated cells"])/int(row["number of nodes"]))
                                            gcRecC.append(float(row["global clustering coeff"]))
                                            trRecC.append(float(row["transitivity"]))
                                        elif an[0] == "AVP":
                                            ccRecA.append(int(row["connected components"]))
                                            isRecA.append(int(row["isolated cells"])/int(row["number of nodes"]))
                                            gcRecA.append(float(row["global clustering coeff"]))
                                            trRecA.append(float(row["transitivity"]))
                                        elif an[0] == "Null":
                                            if an[1] == "CTRL":
                                                NullccRecC.append(int(row["connected components"]))
                                                NullisRecC.append(int(row["isolated cells"])/int(row["number of nodes"]))
                                                NullgcRecC.append(float(row["global clustering coeff"]))
                                                NulltrRecC.append(float(row["transitivity"]))
                                            elif an[1] == "AVP":
                                                NullccRecA.append(int(row["connected components"]))
                                                NullisRecA.append(int(row["isolated cells"])/int(row["number of nodes"]))
                                                NullgcRecA.append(float(row["global clustering coeff"]))
                                                NulltrRecA.append(float(row["transitivity"]))
                                        break # Prevents failure when there is more rows on a file
        ccC[criterion] = ccRecC
        isC[criterion] = isRecC
        gcC[criterion] = gcRecC
        trC[criterion] = trRecC
        ccA[criterion] = ccRecA
        isA[criterion] = isRecA
        gcA[criterion] = gcRecA
        trA[criterion] = trRecA

        NullccC[criterion] = NullccRecC
        NullisC[criterion] = NullisRecC
        NullgcC[criterion] = NullgcRecC
        NulltrC[criterion] = NulltrRecC
        NullccA[criterion] = NullccRecA
        NullisA[criterion] = NullisRecA
        NullgcA[criterion] = NullgcRecA
        NulltrA[criterion] = NulltrRecA

    darkGraph()

    fig, ax = plt.subplots(2,2)
    makeGrpahics(ax[0][0], ccC, ccA, ["Control", "AVP"], 'o')
    makeGrpahics(ax[0][1], isC, isA, ["Control", "AVP"], 'o')
    makeGrpahics(ax[1][0], gcC, gcA, ["Control", "AVP"], 'o')
    makeGrpahics(ax[1][1], trC, trA, ["Control", "AVP"], 'o')

    makeGrpahics(ax[0][0], NullccC, NullccA, ["NullC", "NullA"], '^')
    makeGrpahics(ax[0][1], NullisC, NullisA, ["NullC", "NullA"], '^')
    makeGrpahics(ax[1][0], NullgcC, NullgcA, ["NullC", "NullA"], '^')
    makeGrpahics(ax[1][1], NulltrC, NulltrA, ["NullC", "NullA"], '^')

    secName = ''
    if sections[0] == "1":
        secName = "DM"
    elif sections[0] == "2":
        secName = "V"
    elif sections[0] == "3":
        secName = "DL"
    elif sections[0] == "all":
        secName = "all"

    description = "\nSlice: " + sliceNum[0] + "  -  Section: " + secName
    fig.set_size_inches((10, 10))
    fig.suptitle('Graphs stats' + description, fontsize=16)
    ax[0][0].set_title('Number of connected components (cc)', fontsize=10)
    ax[0][0].spines['top'].set_visible(False)
    ax[0][0].spines['right'].set_visible(False)
    ax[0][0].set_xlabel('Probability of connection')
    ax[0][0].set_ylabel('Number of cc')
    ax[0][0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax[0][1].set_title('Proportion of isolated nodes', fontsize=10)
    ax[0][1].spines['top'].set_visible(False)
    ax[0][1].spines['right'].set_visible(False)
    ax[0][1].set_xlabel('Probability')
    ax[0][1].set_ylabel('Proportion')
    ax[0][1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax[1][0].set_title('Global clustering coefficient', fontsize=10)
    ax[1][0].spines['top'].set_visible(False)
    ax[1][0].spines['right'].set_visible(False)
    ax[1][0].set_xlabel('Probability')
    ax[1][0].set_ylabel('Clustering coefficient')
    ax[1][0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax[1][1].set_title('Transitivity of the network', fontsize=10)
    ax[1][1].spines['top'].set_visible(False)
    ax[1][1].spines['right'].set_visible(False)
    ax[1][1].set_xlabel('Probability')
    ax[1][1].set_ylabel('Transitivity')
    ax[1][1].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    figName = "Null Slice " + sliceNum[0] + "  -  Section " + secName + ' - GT.png'
    dataFolder = "savedData/Results/Generals/"
    fig.savefig(dataFolder + figName, format='png')
    #plt.show()
    plt.close('all')

def main():
    animals     = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1", "Null AVP 1", "Null AVP 2", "Null AVP 3", "Null AVP 4", "Null CTRL 1", "Null CTRL 2", "Null CTRL 3", "Null CTRL 4"]
    sliceNum    = ["1", "2", "3", "4"]
    sliceSide   = ["I", "D"]
    sections    = ["1", "2", "3", "all"]
    fixedRadius = [True]#[True, False]
    criterias   = ["2"]#["1", "2"]
    criterions  = ["0.2000", "0.4285", "0.6000", "0.8000", "0.9000"]

    for sliceN in sliceNum:
        for section in sections:
            if int(sliceN) > 2 and section == "2":
                continue
            generateGraph(animals, [sliceN], sliceSide, [section], fixedRadius, criterias, criterions)

if __name__ == "__main__":
    main()
