spoken = [0,14,6,20,1,4]
#spoken = [0,3,6]

last = spoken[-1]
c = len(spoken) + 1
zeros = 0
numbers= {}
i = 1
for x in spoken:
    numbers[x] = { "a": i, "b": None }
    i+=1

last = 6
while (c <= 30000000): #2020):
    if last in numbers and numbers[last]["b"]:
        diff = abs(numbers[last]["a"]-numbers[last]["b"])
    else:
        diff = 0
            
    if diff not in numbers:
        numbers[diff] = { "a": c, "b": None }        
    else:
        numbers[diff] = { "a": c, "b": numbers[diff]["a"]}
    #print(c,"Saying:", diff)
    last = diff

    if c == 2020:
        print("part 1", last)

    c += 1


print ("part 2", last)   