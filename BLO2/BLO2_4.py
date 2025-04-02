x=int(input("Escribe un número: "))
y=int(input("Escribe otro número: "))
contador=0
while x!=0 or y!=0:
    resx=x%10
    resy=y%10
    if resx==resy:
        contador+=1
    x=x//10
    y=y//10
print("Hay ",contador," dígitos en común.")