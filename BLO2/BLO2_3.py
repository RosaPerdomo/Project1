V=0
N=0
complete=False
while not complete:
    linea=input('Escribe una linea: ')
    trozo=linea.strip('\n').split()
    if len(trozo)!=2:
        print('Error. Escribe un número seguido de V, N o E')
        continue
    num=int(trozo[0])
    letra=trozo[1]
    if letra=='V':
        V+=num
    elif letra=='N':
        N+=num
    elif letra=='E':
        complete=True
Total=V+N
if Total==0:
    print('No se ingresaron votos')
Valido=round((V/Total)*100, 2)
Nulo=round((N/Total)*100, 2)
print('Válidos: ',Valido,'%',', Nulos: ',Nulo, '%')