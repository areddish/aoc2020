def half(s, e, size):
    return [(s,s+size/2-1), (s+size/2, e)]

#with open("test.txt", "rt") as file:
with open("day5.txt", "rt") as file:
    data = [x.strip() for x in file.readlines()]

    ids = []
    for bp in data:
        rs = 0
        re = 127
        row_size = 128

        cs = 0
        ce = 7
        col_size = 8

        for x in bp:
            row_choices = half(rs, re, row_size)
            col_choices = half(cs, ce, col_size)

            if x == 'F':
                rs,re = row_choices[0]
                row_size = row_size // 2
            elif x =='B':
                rs,re = row_choices[1]
                row_size = row_size // 2
            elif x == 'L':
                cs,ce = col_choices[0]
                col_size = col_size // 2
            elif x =='R':
                cs,ce = col_choices[1]
                col_size = col_size // 2

        ids.append(rs * 8 + cs)

print("Part 1", max(ids))

ids.sort()
for x in range(len(ids)-1):
    if ids[x+1] - ids[x] > 1:
        print ("Part 2", ids[x] + 1)
            