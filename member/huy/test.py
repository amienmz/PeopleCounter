__author__ = 'pc'
import time

max = 30000000
sum = 0
first = time.time()
for i in range(0,max):
    if i > -1:
        sum=sum+1
duration = time.time()-first
print " pp: " + str(max/duration) + " p/s"