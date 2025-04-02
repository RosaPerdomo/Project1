n = str(input("Escribe un numero: "))
condicion = False
i=0
while not condicion and i<len(n):
    dec=int(n[i])
    if dec%2!=0:
        condicion = True
    i+=1
    print(condicion)
if condicion == True:
    print("nOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
else:
    print("SIIIIIIIIIIIIII")
