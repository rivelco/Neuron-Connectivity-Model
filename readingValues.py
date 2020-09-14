# Reading script
import csv
import matplotlib.pyplot as plt
import statistics as st
import scipy.stats as stats
import numpy as np

def makeGrpahics(ax, control, avp):
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
        print('Control looks Gaussian (fail to reject H0)')
    else:
    	print('Control does not look Gaussian (reject H0)')
    stat, p = stats.shapiro(dataAVP)
    if p > 0.05:
        print('AVP looks Gaussian (fail to reject H0)')
    else:
    	print('AVP does not look Gaussian (reject H0)')

    diffs = []
    for prob in criterions:
        samp1 = control[prob]
        samp2 = avp[prob]
        stat, p = stats.ttest_ind(samp1, samp2)
        diffs.append(p)

    #ax.scatter(probs, dataControl, marker='o', c='#0000FF', alpha=1, edgecolor='none', label='Control')
    #ax.scatter(probs, dataAVP, marker='o', c='#FF0000', alpha=1, edgecolor='none', label='AVP')
    ax.errorbar(probs, dataControl, yerr=semsControl, marker='o', c='#0000FF', alpha=1, label='Control')
    ax.errorbar(probs, dataAVP, yerr=semsAVP, marker='o', c='#FF0000', alpha=1, label='AVP')
    ax.legend()

    print(diffs)

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

def main():
    animals     = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1"]
    sliceNum    = ["4"]#["1", "2", "3", "4"]
    sliceSide   = ["I", "D"]
    sections    = ["3"]#["1", "2", "3", "all"]
    fixedRadius = [True]#[True, False]
    criterias   = ["2"]#["1", "2"]
    criterions  = ["0.2000", "0.4285", "0.6000", "0.8000", "0.9000"]

    ccC = {}
    isC = {}
    gcC = {}
    trC = {}
    ccA = {}
    isA = {}
    gcA = {}
    trA = {}

    for criterion in criterions:
        ccRecC = []
        isRecC = []
        gcRecC = []
        trRecC = []
        ccRecA = []
        isRecA = []
        gcRecA = []
        trRecA = []
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
        ccC[criterion] = ccRecC
        isC[criterion] = isRecC
        gcC[criterion] = gcRecC
        trC[criterion] = trRecC
        ccA[criterion] = ccRecA
        isA[criterion] = isRecA
        gcA[criterion] = gcRecA
        trA[criterion] = trRecA

    darkGraph()

    fig, ax = plt.subplots(2,2)
    makeGrpahics(ax[0][0], ccC, ccA)
    makeGrpahics(ax[0][1], isC, isA)
    makeGrpahics(ax[1][0], gcC, gcA)
    makeGrpahics(ax[1][1], trC, trA)

    description = "\nSlice: " + sliceNum[0] + "  -  Section: " + sections[0]
    fig.set_size_inches((10, 10))
    fig.suptitle('Graphs stats' + description, fontsize=16)
    ax[0][0].set_title('Number of connected components (cc)', fontsize=10)
    ax[0][0].spines['top'].set_visible(False)
    ax[0][0].spines['right'].set_visible(False)
    ax[0][0].set_xlabel('Probability of connection')
    ax[0][0].set_ylabel('Number of cc')
    ax[0][0].grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    ax[0][1].set_title('Isolated nodes', fontsize=10)
    ax[0][1].spines['top'].set_visible(False)
    ax[0][1].spines['right'].set_visible(False)
    ax[0][1].set_xlabel('Probability')
    ax[0][1].set_ylabel('Isolated nodes')
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

    figName = "Slice: " + sliceNum[0] + "  -  Section: " + sections[0] + ' - GT.png'
    dataFolder = "savedData/Results/Generals/"
    #fig.savefig(dataFolder + figName, format='png')

    plt.show()

if __name__ == "__main__":
    main()
