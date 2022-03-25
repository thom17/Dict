import random

import wordbook
#word = wordbook.Word()

qz = {}
eng =['a', 'b', 'c']
kor = [ ['x', 'ans', 'ans'], ['test', 'ans', 'sd'] , ['ans', 's', 's3', 's2']]
ans = [[1, 2], [1], [0] ]
li = range(5)
print((random.choices(li, k = 4)))

for i in range(3):
    qz[eng[i]] = (kor[i], ans[i])
    #print(qz)

