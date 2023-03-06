from hashlib import blake2b

psw = blake2b()
psw.update(b"admin")

psw2 = blake2b()
psw2.update(b"teste")

print(psw.hexdigest())
print(psw2.hexdigest())
print('---')
print(psw.hexdigest() == psw2.hexdigest())
