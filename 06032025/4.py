num=int(input('dime un nñumero: '))
i=2
suma=1
while i!=num:
    if num%i==0:
        suma+=i
        print(i)
print(suma)