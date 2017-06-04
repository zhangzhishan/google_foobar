#!/usr/bin/env python
# encoding: utf-8

def answer(l, t):
    rets = [-1, -1]
    for i in range(len(l)):
        sum = 0
        for j in range(i, len(l)):
            sum += l[j]
            if sum > t:
                break
            if sum == t:
                rets[0] = i
                rets[1] = j
                return rets
    return rets

