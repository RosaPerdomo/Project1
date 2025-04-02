parties=['PSAO', 'SHDJK', 'PPA', 'ewfwef', 'ywuefj', 'wefuiw']
votes=[45, 23, 6, 3, 8, 23]
x=input('Escribe un partido: ')
i=0
found=False
while i<len(parties) and found==False:
    if parties[i]==x:
        print('The party has',votes[i], 'votes')
        found=True
    else:
        i+=1
if found!=True:
    print('The party is not on the list')