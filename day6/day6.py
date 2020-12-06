#with open("test.txt", "rt") as file:
with open("day6.txt", "rt") as file:
    groups = [x.split("\n") for x in file.read().split("\n\n")]

    people_answered = 0
    people_common = 0

    for group in groups:
        accumulate = set(group[0])
        common = set(group[0])
        for person in group[1:]:
            accumulate |= set(person)
            common = common.intersection(set(person))

        people_answered += len(accumulate)
        people_common += len(common)
    
    print("Part 1", people_answered)
    print("Part 2", people_common)