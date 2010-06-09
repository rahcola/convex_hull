import random
import sys

random.seed(1)
with open(sys.argv[1], 'w') as f:
    for i in range(1, 11):
        for j in range(1, 11):
            if i % 2 == 0:
                f.write('%s %s\n'%(random.randint(-100, 100), random.randint(-100, 100)))
            else:
                f.write('%s %s\n'%((-1**i)*i*9, (-1**j)*j*9))
