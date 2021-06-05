def sub(list1, list2, num):
    out = 0
    for i in range(num):
        tmp = abs(list1[i] - list2[i])
        out += tmp
    return out


def show(list1):
    print(list1)
