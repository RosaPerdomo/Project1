vector=[1,0,23,4,7,7,7,8,4,7,7,7,7,7,4,0,7,1,2]
cuatro=0
siete=0
i=0
while i < len(vector):
    if vector[i]==4:
        cuatro+=1
    elif cuatro==2 and vector[i]==7:
        siete+=1
    i+=1
print(siete)