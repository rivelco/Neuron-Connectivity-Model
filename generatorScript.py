import connectivityModel

def main():
    animals     = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1"]
    nullAnimals = ["Null AVP 1", "Null AVP 2", "Null AVP 3", "Null AVP 4", "Null CTRL 1", "Null CTRL 2", "Null CTRL 3", "Null CTRL 4"]
    sliceNum    = ["1", "2", "3", "4"]
    sliceSide   = ["I", "D"]
    sections    = ["1", "2", "3", "all"]
    fixedRadius = [True]
    criterias   = [1, 2]
    criterions  = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]

    nullContA = {"1":{"1":101, "2":105, "3":96, "all":303}, "2":{"1":107, "2":19, "3":90, "all":216}, "3":{"1":153, "3":118, "all":271}, "4":{"1":152, "3":103, "all":255}}
    nullContC = {"1":{"1":140, "2":68, "3":188, "all":368}, "2":{"1":229, "2":62, "3":247, "all":464}, "3":{"1":231, "3":243, "all":511}, "4":{"1":264, "3":208, "all":472}}
    nullAreas = {"1":{"1":5.97969, "2":2.44852, "3":6.18079, "all":14.0756}, "2":{"1":7.80035, "2":1.76539, "3":7.85442, "all":16.8893}, "3":{"1":8.34064, "3":7.89812, "all":16.7377}, "4":{"1":9.00185, "3":7.85781, "all":16.8597}}

    for animal in nullAnimals:
        for sliceN in sliceNum:
            for sliceS in sliceSide:
                for section in sections:
                    if int(sliceN) > 2 and section == "2":
                        continue
                    for fRad in fixedRadius:
                        for criteria in criterias:
                            for criterion in criterions:
                                an = animal.split()
                                if an[1] == "AVP":
                                    cont = nullContA[sliceN][section]
                                elif an[1] == "CTRL":
                                    cont = nullContC[sliceN][section]
                                area = nullAreas[sliceN][section]
                                connectivityModel.main(animal, sliceN+sliceS, section, fRad, criteria, criterion, True, cont, area)
                                if len(criterions) > 1 and criteria == 1:
                                    break

    exit() # useful when only making null models

    for animal in animals:
        for sliceN in sliceNum:
            for sliceS in sliceSide:
                for section in sections:
                    for fRad in fixedRadius:
                        for criteria in criterias:
                            for criterion in criterions:
                                connectivityModel.main(animal, sliceN+sliceS, section, fRad, criteria, criterion)
                                if len(criterions) > 1 and criteria == 1:
                                    break
if __name__ == "__main__":
    main()
