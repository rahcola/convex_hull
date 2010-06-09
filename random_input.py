import random
import sys

with open(sys.argv[1], 'w') as f:
    for i in range(1, 11):
        for j in range(1, 11):
            f.write('%s %s\n'%(random.randint(1, 100), random.randint(1, 100)))
