x=int(input("Escribe un número: "))
num=1
sum=0
while num<x:
    if x%num==0:
        sum=sum+num
    num+=1
if sum==x:
    print("És un nombre perfecte")
else:
    print("No és un nombre perfecte")