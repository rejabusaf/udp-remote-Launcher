

def gridGate1(d2, d1, d0):

    instanceNum = 0

    if bool(int(d2)) is False:
        gridGate0(d1, d0, instanceNum)
    else:
        instanceNum += 4
        gridGate0(d1, d0, instanceNum)


def gridGate0(d1, d0, instanceNum):

    if bool(int(d1)) is False:

        if bool(int(d0)) is False:
            instanceNum += 1
            print(instanceNum)
            return instanceNum

        else:
            instanceNum += 2
            print(instanceNum)
            return instanceNum

    else:

        if bool(int(d0)) is False:
            instanceNum += 3
            print(instanceNum)
            return instanceNum

        else:
            instanceNum += 4
            print(instanceNum)
            return instanceNum

temp = '0b{}'
print(str(temp))
capturedStr = "1$1$0"

d2, d1, d0 = capturedStr.split('$')
print('d2=', d2, 'd1=', d1, 'd0=', d0)
gridGate1(d2, d1, d0)

