x=int(input("Escribe un número:"))
y=int(input("Escribe otro número:"))
if y<0:
    print('Error en los datos de entrada')
res=1
cont=1
nose=x**y
print(nose)
while cont<=y:
    res=res*x
    cont+=1
print("El resultado es:",res)
