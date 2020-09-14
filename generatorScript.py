import connectivityModel

def main():
    animals     = ["AVP 6 L1", "Control 6 L1", "AVP 3 L1", "Control 07J L1"]
    sliceNum    = ["1", "2", "3", "4"]
    sliceSide   = ["I", "D"]
    sections    = ["1", "2", "3", "all"]
    fixedRadius = [True]
    criterias   = [1, 2]
    criterions  = [0.2000, 0.4285, 0.6000, 0.8000, 0.9000]

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
