import connectivityModel
import sys

# This function generates the data for all the experimental and null animals
# DISCLAIMER: may take a while to finish, couple of hours
# Receives one arguments when the function is called, may be:
#   all - To analyze experimental and null animals
#   exp - To analyze only experimental, real animals
#   nul - To analyze only null animals
# The function by itself does not creates files, it only runs the connectivityModel.py with
# all the possible configurations
def main():
    all = False     # Initializing the arguments
    exp = False
    nul = False

    if sys.argv[1] == "all":        # Evaluate the kind of analysis
        all = True
    elif sys.argv[1] == "exp":
        exp = True
    elif sys.argv[1] == "nul":
        nul = True
    else:                           # If not a valid arg, then the program finish
        print("Not a valid argument passed. Did nothing.")
        exit()

    animals     = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1"]    # Exp animals
    nullAnimals = ["Null AVP 1", "Null AVP 2", "Null AVP 3", "Null AVP 4",      # Null animals
                   "Null CTRL 1", "Null CTRL 2", "Null CTRL 3", "Null CTRL 4"]
    sliceNum    = ["1", "2", "3", "4"]              # Slices
    sliceSide   = ["I", "D"]                        # Sides
    sections    = ["1", "2", "3", "all"]            # Anatomic section inside nucleus
    fixedRadius = [True]                            # Only for fixed radius configuration
    criterias   = [1, 2]                            # One of the two possible criterias
    criterions  = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]  # Criterions for criteria 2

    # Dictionaries for the average number of cells per group, per slice and per region or section
    # This are used only when making null models. Data based on experimental data
    nullContA = {"1":{"1":101, "2":105, "3":96, "all":303},     # Count for AVP group
                 "2":{"1":107, "2":19, "3":90, "all":216},
                 "3":{"1":153, "3":118, "all":271},
                 "4":{"1":152, "3":103, "all":255}}
    nullContC = {"1":{"1":140, "2":68, "3":188, "all":368},     # Count for Control group
                 "2":{"1":229, "2":62, "3":247, "all":464},
                 "3":{"1":231, "3":243, "all":511},
                 "4":{"1":264, "3":208, "all":472}}
    nullAreas = {"1":{"1":5.97969, "2":2.44852, "3":6.18079, "all":14.0756},    # Area for nuclei
                 "2":{"1":7.80035, "2":1.76539, "3":7.85442, "all":16.8893},
                 "3":{"1":8.34064, "3":7.89812, "all":16.7377},
                 "4":{"1":9.00185, "3":7.85781, "all":16.8597}}

    # Evaluating for experimental animals
    if exp or all:
        for animal in animals:
            for sliceN in sliceNum:
                for sliceS in sliceSide:
                    for section in sections:
                        # Beyond the slice 2, there's not a ventral region (identified by 2)
                        if int(sliceN) > 2 and section == "2":
                            continue
                        for fRad in fixedRadius:
                            for criteria in criterias:
                                for criterion in criterions:
                                    inData = {}             # Dictionary with input data
                                    inData["animal"]        = animal
                                    inData["slice"]         = sliceN+sliceS
                                    inData["section"]       = section
                                    inData["fixedRadius"]   = fRad
                                    inData["criteria"]      = criteria
                                    inData["criterion"]     = criterion
                                    inData["nullModeling"]  = False
                                    inData["saveCSV"]       = True
                                    inData["saveFigs"]      = True
                                    inData["showFigs"]      = False

                                    connectivityModel.main(inData)  # Run the analysis

                                    # The criteria 1 does not use criterions, so skip the rest of it
                                    if len(criterions) > 1 and criteria == 1:
                                        break
    # Analyzing the null animals
    if nul or all:
        for animal in nullAnimals:
            for sliceN in sliceNum:
                for sliceS in sliceSide:
                    for section in sections:
                        if int(sliceN) > 2 and section == "2":
                            continue
                        for fRad in fixedRadius:
                            for criteria in criterias:
                                for criterion in criterions:
                                    an = animal.split() # identify the group to pick the count
                                    if an[1] == "AVP":
                                        cont = nullContA[sliceN][section]   # From AVP group
                                    elif an[1] == "CTRL":
                                        cont = nullContC[sliceN][section]   # From Control group
                                    area = nullAreas[sliceN][section]  # Area is the same for both

                                    inData = {}
                                    inData["animal"]        = animal
                                    inData["slice"]         = sliceN+sliceS
                                    inData["section"]       = section
                                    inData["fixedRadius"]   = fRad
                                    inData["criteria"]      = criteria
                                    inData["criterion"]     = criterion
                                    inData["nullModeling"]  = True
                                    inData["noc"]           = cont
                                    inData["nullArea"]      = area
                                    inData["saveCSV"]       = True
                                    inData["saveFigs"]      = True
                                    inData["showFigs"]      = False

                                    connectivityModel.main(inData)

                                    if len(criterions) > 1 and criteria == 1:
                                        break

if __name__ == "__main__":
    # Must be run with an argument, either 'all', 'exp' or 'nul'
    main()
