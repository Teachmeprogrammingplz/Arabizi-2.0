# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:18:04 2022

@author: m.echchihab
"""



from hashlib import blake2b, sha256
h = sha256()
h2 = blake2b()
h.update(b"Bonjour")
h2.update(b"Bonjour")
HashOfThing = h.hexdigest()
print("Has256(Bonjour)=", HashOfThing)
HashOfThing2 = h2.hexdigest()
print("Blake2b(Bonjour)=", HashOfThing2)



