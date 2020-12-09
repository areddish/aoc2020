def has_sum(array, num):
    for x in range(len(array)):
        if num - array[x] in array:
            return True
    return False
        
    
#with open("test.txt", "rt") as file:
with open("day9.txt", "rt") as file:
    data = [int(x) for x in file.read().splitlines()]
    data_len = len(data)

    part1_answer = 0
    preamble = 25
    window_start = 0
    for x in data[preamble:]:
        if not has_sum(data[window_start:window_start+preamble], x):
            part1_answer = x
            break
        window_start += 1

    print ("Part 1", part1_answer)

    for x in range(1, data_len):
        running_sum = data[x]
        y = x + 1
        while (y < data_len and running_sum < part1_answer):
            running_sum += data[y]
            y += 1

        if running_sum == part1_answer:
            print("Part 2", min(data[x:y]) + max(data[x:y]))
            break