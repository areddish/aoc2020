#with open("test.txt", "rt") as file:
with open("day6.txt", "rt") as file:
    data = file.read().splitlines()

    people_answered = 0
    people_common = 0

    accumulate = set()
    common = None
    for line in data:
        if line == "":
            people_answered += len(accumulate)
            people_common += len(common)
            accumulate = set()
            common = None
        else:
            accumulate |= set(line)
            if common != None:
                common = common.intersection(set(line))
            else:
                common = set(line)
    
    print("Part 1", people_answered)
    print("Part 2", people_common)