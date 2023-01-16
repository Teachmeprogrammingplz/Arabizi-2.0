# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:18:04 2022

@author: m.echchihab
"""


'''
from hashlib import blake2b, sha256
h = sha256()
h2 = blake2b()
h.update(b"Bonjour")
h2.update(b"Bonjour")
HashOfThing = h.hexdigest()
print("Has256(Bonjour)=", HashOfThing)
HashOfThing2 = h2.hexdigest()
print("Blake2b(Bonjour)=", HashOfThing2)
'''



import numpy as np
import matplotlib.pyplot as plt
import math
import libnum

def courbeCarré(a,b,p,x):
    return (pow(x, 3) + a*x + b) % p

def pointsCourbe(a,b,p):
    X=[]
    Y=[]
    for x in range(p):
        y2=courbeCarré(a,b,p,x)
        print("x=", x, "y2=", y2)
        for k in range(p):
            r = math.sqrt(y2)
            print("    k=", k, "y2", y2, "r=", r)
            if r.is_integer():
                X.append(x)
                Y.append(r)
            y2 += p
    return X,Y

def additionECC(a,b,p, P, Q):
    #    print("P=",P, "Q=", Q, "p=", p)
    if P == [0]:
        return Q
    elif Q == [0]:
        return P
    elif (P != Q and P[0] == Q[0]):
        return [0]
    elif P == Q:
        s = ((3 * (P[0] ** 2) + a) * libnum.invmod(a * P[1], p)) % p
    else:
        s = ((P[1] - Q[1]) * libnum.invmod(P[0] - Q[0], p)) % p
    R = [0, 0]
    R[0] = (s ** 2 - (P[0] + Q[0])) % p
    R[1] = (s * (P[0] - R[0]) - P[1]) % p
    return R

def main():
    a = 6
    b = 4
    p = 7

    plt.figure()
    plt.title('Courbes elliptiques')

    y, x = np.ogrid[-10:10:100j, -10:10:100j]
    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    plt.grid()
    plt.show()

    x, y = pointsCourbe(a,b,p)
#    plt.figure(figsize=(12,8))
    plt.subplot(2,1,1)
    plt.plot(x,y,'ro')

    x=np.linspace(0,2,10)
    y=x**2
    plt.subplot(2,1,2)
    plt.plot(x,y,label='quadratique', c='red')
    plt.xlabel('axe x')
    plt.ylabel('axe y')
    plt.legend()
    plt.show()
    plt.savefig('courbesElliptiques')
#    plt.savf

if __name__ == '__main__':
    main()