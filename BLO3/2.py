before=0
after=0
contador=0
n=int(input("Escribe un número: \n"))
while n!=0:
    if n==100:
        contador+=1
    elif contador==0:
        before+=n
    elif contador==3:
        after+=n
    n = int(input("Escribe otro número: \n"))
    sum=before+after
print("la suma entre", before, 'y', after, 'es', sum)