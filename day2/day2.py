with open("day2.txt", "rt") as file:
    data = file.readlines()

    valid = 0
    valid2 = 0
    for entry in data:
        parts = entry.split(' ')
        limits = parts[0].split('-')
        letter = parts[1].split(':')[0]
        password = parts[2]
        count = 0
        for ch in password:
            if ch == letter:
                count += 1

        if (count >= int(limits[0]) and count <= int(limits[1])):
            valid += 1

        if (password[int(limits[0])-1] == letter or password[int(limits[1])-1] == letter):
            if (not password[int(limits[0])-1] == password[int(limits[1])-1]):
                valid2 += 1
    print(valid, valid2)

