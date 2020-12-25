with open("day25.txt") as file:
    lines = file.read().splitlines()
    pub_keys = [ int(lines[0]), int(lines[1])]

    loop_size = 1
    val = 1
    enc_key = 1
    while val not in pub_keys:
        val *= 7
        val = val % 20201227

        enc_key *= pub_keys[0]
        enc_key = enc_key % 20201227
        loop_size += 1

    print("enc key = ", enc_key)