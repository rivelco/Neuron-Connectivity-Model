import connectivityModel

def main():
    animals     = ["AVP 3 L1", "AVP 6 L1", "Control 6 L1", "Control 07J L1"]
    sliceNum    = ["1", "2", "3", "4"]
    sliceSide   = ["I", "D"]
    sections    = ["1", "2", "3", "all"]
    fixedRadius = [True, False]
    criterias   = [1, 2]
    criterions  = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]

    #connectivityModel.main("Control 6 L1", "1D", "all", False, 1, 0.2)

    #exit()

    for animal in animals:
        for sliceN in sliceNum:
            for sliceS in sliceSide:
                for section in sections:
                    for fRad in fixedRadius:
                        for criteria in criterias:
                            for criterion in criterions:
                                #print("connectivityModel.py", animal, sliceN+sliceS, section, fRad, criteria, criterion)
                                connectivityModel.main(animal, sliceN+sliceS, section, fRad, criteria, criterion)

if __name__ == "__main__":
    main()
