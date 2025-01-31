# 

from jwt import JWT
key = 'testkey'

encoded = JWT().encode({"id": 1111}, alg="HS256")
print(encoded)
