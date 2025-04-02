frase=input("Escribe una frase: \n")
frase=list(frase)
i=0
while frase[i]!='.':
    if (frase[i]=='x') or (frase[i]=='X'):
        j=i
        while (frase[j])!='.':
            frase[j]=frase[j+1]
            j+=1
    else:
        i+=1
print(frase)