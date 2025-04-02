num=int(input('Dime un número: '))
par=0
impar=0
while num!=0:
    dec=num%10
    if dec%2==0:
        par+=1
    else:
        impar+=1
    num=num//10
if par==impar:
    print('Sí')
else:
    print('No')