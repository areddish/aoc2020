def half(s, e, size):
    return [(s,s+size/2-1), (s+size/2, e)]

#with open("test.txt", "rt") as file:
with open("day5.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    ids = []
    for bp in data:
        s = 0
        e = 127
        size = 128
        for x in bp[:7]:
            choices = half(s,e, size)
            if x == 'F':
                s,e = choices[0]
            elif x =='B':
                s,e = choices[1]
            size = size // 2
        row = s

        s = 0
        e = 7
        size = 8
        for r in bp[7:]:
            choices = half(s,e, size)
            if r == 'L':
                s,e = choices[0]
            elif r =='R':
                s,e = choices[1]
            size = size // 2
        ids.append(row * 8 + s)

print("Part 1", max(ids))

ids.sort()
for x in range(128*8):
    if x+1 in ids and x-1 in ids and not x in ids:
        print ("Part 2", x)
            