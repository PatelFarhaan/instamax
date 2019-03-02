def accept(n):
    var1 = int(n / 15)
    if n % 15:
        var1 = int(var1 + 1)

    for j in range(0, var1):

        for i in range(1, 16):
            print(i)
    print( "{} Requests Accepted".format(n))


accept(45)