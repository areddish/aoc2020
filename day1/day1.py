with open("day1.txt", "rt") as file:
    data = [int(x) for x in file.readlines()]

    lookup = { 2020-x:x for x in data}
    for x in data:
        y = lookup.get(x, None)
        if y:
            print("Part 1: ", x * y)
            break
            
    for i in range(0,len(data)):
        for j in range(i+1,len(data)):
            for k in range(j+1,len(data)):
                if (data[i] + data[j] + data[k]) == 2020:
                    print("Part 2:", data[i]*data[j]*data[k])
                    exit(-1)


