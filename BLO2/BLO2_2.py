X=int(input("Escribe un número: "))
sum=0
while X>0:
    res=X%10
    sum+=res
    X=X//10
print(sum)