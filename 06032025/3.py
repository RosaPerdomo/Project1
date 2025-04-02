n=int(input('Escribe un número: '))
m=0
condicion=False
while m!=-1 and condicion==False:
    m=int(input('Escribe otro número: '))
    if n>=m:
        condicion=True
        print('si')
        continue
    n=m
if condicion==True:
    print('No es creciente')
else:
    print('Es creciente')