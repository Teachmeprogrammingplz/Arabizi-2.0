# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 19:02:18 2022

@author: m.echchihab
"""

IX = int(input("Entrer le germe IX : "))
IY = int(input("Entrer le germe IY : "))
IZ = int(input("Entrer le germe IZ : "))


def alea() : 
    global IX
    global IY
    global IZ
    
    IX = 171 * ( IX % 177 ) - 2 * ( IX // 177 ) 
    IY = 172 * ( IY % 176 ) - 35 * ( IY // 176 )
    IZ = 170 * ( IZ % 178 ) - 63 * ( IZ // 178 )
    
    if IX < 0 : 
        IX += 30269
    if IY < 0 : 
        IY += 30307
    if IZ < 0 :
        IZ += 30323
    
    inter = ( ( IX / 30269 ) + ( IY / 30307 ) + ( IZ / 30323 ) )
    alea = inter - int(inter)
    
    #pour lesser seulement 4 chiffres apres la virgule
    alea =  "{:.4f}".format(alea)

    return alea

res = []

for i in range(100) :
    res.append(alea())
    
print("\n\nla lise des 100 valeurs aleatoires sont : " )
print(res)