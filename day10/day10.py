#with open("test.txt", "rt") as file:
with open("day10.txt", "rt") as file:
    data = [int(x) for x in file.read().splitlines()]
    data_len = len(data)

    data.sort()
    m = max(data)
    data = [0] + data + [m+3]

    diff = { 1: 0, 3: 0}
    for x in range(len(data)-1):
        diff[data[x+1]-data[x]] += 1
    
    print("Part 1", diff[1] * diff[3])

    # find runs and group them
    runs = []
    i = 1
    while (i < len(data) - 1):
        run = [data[i]]
        while (data[i+1] - data[i] == 1):
            run.append(data[i+1])
            i+=1
        runs.append(run)
        i += 1

    # trim the ends, as the boundaries between runs are difference
    # of three and thus we have to keep those values.
    runs[0] = runs[0][:-1]
    for x in range(1,len(runs)):
        runs[x] = runs[x][1:-1]

    # compute combinations based on group size of numbers we have
    # left to modify.
    combinations = 1
    for x in runs:
        numbers = len(x)
        if numbers == 3:
            # 2^3 - 1, because you can't eliminate all three
            combinations *= 7
        elif numbers == 2:
            # 2^2 combinations - both, none, first, second
            combinations *= 4
        elif numbers == 1:
            # 2^1 combinations - all or none
            combinations *= 2
    print("Part 2", combinations)
