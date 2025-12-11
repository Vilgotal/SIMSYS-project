def functionr(x):
    return x+1

def functions(x):
    return x+3

x = 1

lst = [lambda: functionr(x), lambda: functions(x)]
for i in range(0,3):
    for f in lst:
        r = f()
        print(r)