# Reading script
import csv
import matplotlib.pyplot as plt
import statistics as st
import scipy.stats as stats
import numpy as np
import sys
import pathlib

# This function creates the actual plot with error bars and saves the data plotted
# Receive a matplotlib ax, control and AVP data (dict of lists), the marker and name for csv file
# Creates the plot on ax and saves 4 csv files with plotted data
def makeGrpahics(ax, control, avp, mark, csvName):
    criterions  = ["0.2000", "0.4285", "0.6000", "0.8000", "0.9000"]    # To identify the dicts
    probs = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]                    # x axes

    listControl = []  # Will store the average of each probability for CTRLs
    semsControl = []  # Will store the standard error of the mean of each probability for CTRLs
    for prob, values in control.items():        # Fills the previous lists
        listControl.append(st.mean(values))
        semsControl.append(stats.sem(values))

    listAVP = []      # Will store the average of each probability for AVPs
    semsAVP = []      # Will store the standard error of the mean of each probability for AVPs
    for prob, values in avp.items():    # Fills the previous lists
        listAVP.append(st.mean(values))
        semsAVP.append(stats.sem(values))

    dataControl = np.array(listControl) # Converts the lists as numpy arrays
    dataAVP     = np.array(listAVP)

    diffs = []                          # To store the p values for each comparative
    for prob in criterions:             # Evaluates for all the criterions
        samp1 = control[prob]               # Selects the samples
        samp2 = avp[prob]
        stat, p = stats.ttest_ind(samp1, samp2) # T-student comparative
        diffs.append(p)                 # Stores the p value for that comparation

    headers = ['C 0.2000', 'A 0.2000', 'C 0.4285', 'A 0.4285', 'C 0.6000',  # Headers of each file
               'A 0.6000', 'C 0.8000', 'A 0.8000', 'C 0.9000', 'A 0.9000']

    dataFolder = "savedData/Results/Generals/"   # Folder where the csv files will be saved
    pathlib.Path(dataFolder).mkdir(parents=True, exist_ok=True) # Creates the folder path
    with open(dataFolder + '/' + csvName + '.csv', mode='a') as csv_file: # Open the file
        writer = csv.writer(csv_file)               # csv writer
        writer.writerow(headers)                    # Write the headers
        for i in range(len(control['0.2000'])):     # Iterates over all the samples, equal per group
            newRow = []                             # Temporary new row
            for c in criterions:                    # Iterates over all criterions
                newRow.append(control[c][i])            # Append CTRL and AVP per iteration
                newRow.append(avp[c][i])
            writer.writerow(newRow)                 # Writes the row

    labelC = 'CTRL'                 # Label for each series for the plot
    labelA = 'AVP'
    if csvName[0] == 'N':           # Preppends 'Null' if null modeling
        labelC = 'Null ' + labelC
        labelA = 'Null ' + labelA

    # Makes the actual plots with error bars with specified mark and label
    ax.errorbar(probs, dataControl, yerr=semsControl, marker=mark, c='#0000FF', label=labelC)
    ax.errorbar(probs, dataAVP, yerr=semsAVP, marker=mark, c='#FF0000', label=labelA)
    for i, tag in enumerate(range(len(dataControl))):
        ax.annotate("{:.4f}".format(diffs[i]), (probs[i], dataControl[i]))  # p-values as labels
    ax.legend() # Adds the legend in the plot

# This function sets the plots styles, dark mode
def darkPlot():
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

# Function that makes the plots
# Receives the data for the animal
# Generates a plot, also 4 csv files with the numeric data plotted
def generatePlot(animals, sliceNum, sliceSide, section, fRad, criteria, criterions, nullM):
    data = {'Control'   : {'cc': {}, 'is': {}, 'gc': {}, 'tr': {}}, # Data structure for everything
            'AVP'       : {'cc': {}, 'is': {}, 'gc': {}, 'tr': {}},
            'NullCTRL'  : {'cc': {}, 'is': {}, 'gc': {}, 'tr': {}},
            'NullAVP'   : {'cc': {}, 'is': {}, 'gc': {}, 'tr': {}}}

    for animal in ['Control', 'AVP', 'NullCTRL', 'NullAVP']:    # Creates a list for every criterion
        for category in ['cc', 'is', 'gc', 'tr']:
            for criterion in criterions:
                data[animal][category][criterion] = []

    for criterion in criterions:   # Iterates over criterions, slice sides and animals
        for sliceS in sliceSide:
            for animal in animals:
                # Searches over the saved data, generated by connectivityModel.py
                folderPath = "oldSavedData/" + animal + "/Criteria " + criteria + "/"
                folderPath += criterion + "/" + sliceNum + sliceS + "/" + section + "/"
                fileName = animal + " - GT.csv"
                location = folderPath + fileName
                an = animal.split()                 # To identify the group of the animal
                with open(location) as file:        # Open the file at given location
                    reader = csv.DictReader(file)   # Reads as a dictionary
                    for row in reader:              # Reads out each row
                        group = an[0]
                        if an[0] == 'Null':         # Identifies the null groups
                            group += an[1]
                        # Added the data to the corresponding structure
                        propIsolated = int(row["isolated cells"])/int(row["number of nodes"])
                        data[group]['cc'][criterion].append(int(row["connected components"]))
                        data[group]['is'][criterion].append(propIsolated)
                        data[group]['gc'][criterion].append(float(row["global clustering coeff"]))
                        data[group]['tr'][criterion].append(float(row["transitivity"]))
                        break # Prevents failure when there is more rows on a file

    darkPlot()              # Formats the plot

    secName = ''            # Identifies the number of section with the correct abbreviation
    if section == "1":
        secName = "DM"
    elif section == "2":
        secName = "V"
    elif section == "3":
        secName = "DL"
    elif section == "all":
        secName = "all"

    fig, ax = plt.subplots(2,2)                     # Creates the plots
    csvName = 'S ' + sliceNum + ' - R ' + secName   # Creates the csv file name

    if not nullM:
        # Makes the plots for all the data, pairing controls vs AVP treated animals
        makeGrpahics(ax[0][0], data['Control']['cc'], data['AVP']['cc'], 'o', csvName + ' CC')
        makeGrpahics(ax[0][1], data['Control']['is'], data['AVP']['is'], 'o', csvName + ' IS')
        makeGrpahics(ax[1][0], data['Control']['gc'], data['AVP']['gc'], 'o', csvName + ' GC')
        makeGrpahics(ax[1][1], data['Control']['tr'], data['AVP']['tr'], 'o', csvName + ' TR')

    if nullM:                                       # True if including null model
        csvName = 'Null-' + csvName                 # Prepends 'Null' to csv file
        makeGrpahics(ax[0][0], data['NullCTRL']['cc'], data['NullAVP']['cc'], '^', csvName + ' CC')
        makeGrpahics(ax[0][1], data['NullCTRL']['is'], data['NullAVP']['is'], '^', csvName + ' IS')
        makeGrpahics(ax[1][0], data['NullCTRL']['gc'], data['NullAVP']['gc'], '^', csvName + ' GC')
        makeGrpahics(ax[1][1], data['NullCTRL']['tr'], data['NullAVP']['tr'], '^', csvName + ' TR')

    # Style and info for the plot
    description = "\nSlice: " + sliceNum + "  -  Section: " + secName
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

    figName = "Slice " + sliceNum + "  -  Section " + secName + ' - GT.png' # Figure name
    if nullM:                           # True if null modeling
        figName = 'Null ' + figName
    dataFolder = "savedData/Results/Generals/"      # Folder where the figure will be saved
    fig.savefig(dataFolder + figName, format='png') # Figure is saved
    #plt.show()
    plt.close('all')

# Main function, generates the graphics and the csv files with plotted data
# Receives one argument by the console, either 'nullModel' or 'justExp'
#   indicating if the null model must be plotted too.
# The function saves the plots and the csv files with the numeric data
def main():
    n = sys.argv[1]         # Extract the argument and evaluates if include null model or not
    if n == 'nullModel':
        n = True
    elif n == 'justExp':
        n = False
    else:
        print('Not a valid parameter. Did nothing')
        exit()

    if n:
        animals = ["Null AVP 1", "Null AVP 2", "Null AVP 3", "Null AVP 4",     # Null animals
                   "Null CTRL 1", "Null CTRL 2", "Null CTRL 3", "Null CTRL 4"]
    else:
        animals = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1"]    # Real animals
    sliceNum    = ["1", "2", "3", "4"]                  # Number of slices
    sliceSide   = ["I", "D"]                            # Slice sides
    sections    = ["1", "2", "3", "all"]                # Anatomical regions of the nuclei
    fixedRadius = True                                  # True if radius considered as fixed
    criteria    = '2'                                   # Criteria evaluating
    criterions  = ["0.2000", "0.4285", "0.6000", "0.8000", "0.9000"]    # Different criterions

    print(">> Adding null models: " + str(n))
    # Iterates over the different slices and sections
    for sliceN in sliceNum:
        for section in sections:
            if int(sliceN) > 2 and section == "2":  # Beyond slice 2 there's not section 2
                continue
            print(">> Analyzing slice: " + sliceN + " - Section: " + section)
            generatePlot(animals, sliceN, sliceSide, section, fixedRadius, criteria, criterions, n)

if __name__ == "__main__":
    main()
