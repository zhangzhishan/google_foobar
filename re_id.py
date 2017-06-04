#!/usr/bin/env python
# encoding: utf-8
import math
def answer(n):
    if n == 0:
        return '23571'
    cnt = 0
    ret = '2'
    start = 3
    while cnt < n + 5:
        is_prime = True
        for i in xrange(3, int(math.ceil(math.sqrt(start + 1))) + 1):
            if start % i == 0:
                is_prime = False
                break
        if is_prime:
            cnt += len(str(start))
            ret += str(start)
        start += 2
    return ret[n:n + 5]

if __name__ == "__main__":
    for i in xrange(20):
        print answer(i)
    print answer(10000)
    print answer(3241)