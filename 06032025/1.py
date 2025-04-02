linea=int(input("Escribe tres números separados por un espacio:\n"))
trozo=linea.split(' ')
if trozo[0]==trozo[1]:trozo[0]==trozo[1] and trozo[1]==trozo[2]:
    print('Error')
elif trozo[1]==trozo[2]:
    print(trozo[1])
elif trozo[0]==trozo[2]:
    print(trozo[2])
elif trozo[0]==trozo[1]:
    print(trozo[0])
else:
    print('No')