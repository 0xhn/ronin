from utils.db import db
from bson import ObjectId
import math
from utils.contact_decoder import contact
'''
根据id查询记录

result = db['axiecontact_transfer'].find_one({'_id': ObjectId('61a653fb16ba7222d992e5c3')})
print(result)
'''

'''
分页代码
axie_trans = list(db['axiecontact_transfer'].find(
    {},
    {'_id': 1, 'input': 1, 'token_id': 1}).limit(10000).skip(2000000).sort([('_id', 1)]))
print(axie_trans)
'''

'''
解码代码
result = contact.decode_function_input('0x4d51bfc40000000000000000000000003b389940949895807e66d25c83cd79c60b8d1536000000000000000000000000c99a6a985ed2cac1ef41640596c5a5f9f4e19ef5000000000000000000000000000000000000000000000000006a94d74f430000000000000000000000000000000000000000000000000000000000000068b1484b78022c7d209c3a40389b3e191df1d0636f0384d153aecbe83ec10f4e47d103')
print(result[1])
'''

'''
测试取整
a = 8
b =3
print(math.ceil(a/b))
'''

