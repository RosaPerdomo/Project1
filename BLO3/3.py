frase=input("Escribe una frase: \n")
frase=list(frase)
i=0
while frase[i]!=".":
    if i%2==0 and frase[i+1]!=".":
        save=frase[i]
        frase[i]=frase[i+1]
        frase[i+1]=save
    i+=1
print(frase)