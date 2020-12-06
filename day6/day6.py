#with open("test.txt", "rt") as file:
with open("day6.txt", "rt") as file:
    data = file.read().splitlines()

    people_answered = []
    people_common = []

    group = {}
    current = None
    for line in data:
        if line == "":
            people_answered.append(len(group))
            people_common.append(len(current))
            group = {}
            current = None
        else:
            for x in list(line):
                group[x] = True
            if current != None:
                current = current.intersection(set(line))
            else:
                current = set(line)
    
    print("Part 1", sum(people_answered))
    print("Part 2", sum(people_common))