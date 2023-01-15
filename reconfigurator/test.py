def test():
    for i in [1,2,3,4]:
        yield i
    
def outloop():
    for j in [1,2,3]:
        yield (list(test()))

for i in outloop():
    print(i)
