def check_hgt(h):
    if "cm" in h:
        return 150 <= int(h.replace("cm","")) <= 193
    elif "in" in h:
        return 59 <= int(h.replace("in","")) <= 76
    else:
        return False
        
def check_hcl(h):
    if h[0] != '#' or len(h) != 7:
        return False
    for x in h[1:]:
        if not x in list("abcdef0123456789"):
            return False
    return True

def check_range(v, low, high):
    return low <= int(v) <= high

validation = {
    "hgt": check_hgt,
    "hcl": check_hcl,
    "pid": lambda x: len(x) == 9,
    "byr": lambda x: check_range(x, 1920, 2002),
    "iyr": lambda x: check_range(x, 2010, 2020),
    "eyr": lambda x: check_range(x, 2020, 2030),
    "ecl": lambda x: x in ["amb","blu","brn","gry", "grn", "hzl", "oth"],
    "cid": lambda x: True
}

def validate_passport(p):
    return len(p) == 8 or (len(p) == 7 and not p.get("cid", None))

#with open("test.txt", "rt") as file:
with open("day4.txt", "rt") as file:
    valid = 0
    valid2 = 0
    passport = {}
    passport2 = {}
    for l in file.read().splitlines():
        if l.strip() == "":
            valid += validate_passport(passport)
            valid2 += validate_passport(passport2)
            passport = {}
            passport2 = {}
        else:
            for x in l.strip().split(' '):
                p = x.split(":")
                passport[p[0]] = p[1]
                if (validation[p[0]](p[1])):
                    passport2[p[0]] = p[1]

    valid += validate_passport(passport)
    valid2 += validate_passport(passport2)

    print (valid)
    print (valid2)
