#!/usr/bin/env python
# encoding: utf-8
from fractions import Fraction, gcd
import copy
import itertools


class Matrix(list):
    def __init__(self, values):
        super(Matrix, self).__init__(values)

    def shape(self):
        i_length = len(self)
        j_length = len(self[0])
        return (i_length, j_length)

# 转置
def transpose(M):
    _tmp = zip(*M)
    return Matrix([list(_l) for _l in _tmp])

# 阵乘
def multiplyMatrix(M1, M2):
    M1 = Matrix(M1)
    M2 = Matrix(M2)
    m, x1 = M1.shape()
    x2, n = M2.shape()

    productF = lambda item: item[0]*item[1]
    M2 = transpose(M2)
    returnMatrix = []
    for l_list in M1:
        _tmpList = []
        returnMatrix.append(_tmpList)
        for r_list in M2:
            value = sum([ productF(item) for item in zip(l_list, r_list)])
            if abs(round(value) - value) < 0.00001: value = int(round(value))
            _tmpList.append(value)
    return Matrix(returnMatrix)

# 数乘
def multiplyNumber(N, M):
    _M = copy.deepcopy(M)
    _N = (N)
    _M = [
        [ value*_N for value in _l ]
        for _l in _M
    ]
    return Matrix(_M)


# 行列式
def getDeterminant(M):
    # 杜尔里特算法（Doolittle algorithm）
    M = Matrix(M)
    m, n = M.shape()
    j_indexer = itertools.cycle(range(n))
    minusF = lambda rate, item: item[0] + (rate * item[1])
    product = 1
    for i in range(m):
        j = j_indexer.next()
        base = (M[i][j])
        _count = 0
        here_to_tail_span = m-i-1
        while base == 0 and _count<here_to_tail_span:
            product *= (-1)**here_to_tail_span
            _count += 1
            M.append(M.pop(i))
            base = (M[i][j])
        if base == 0: return 0
        product *= base
        _i = i
        _j = j
        while _i < m-1:
            _i += 1
            _base = (M[_i][_j])
            if _base == 0: continue
            rate = -(_base/base)
            M[_i] = [minusF(rate, item) for item in zip(M[_i], M[i])]
    return product

# 伴随矩阵
def getAdjugateMatrix(M):
    length = len(M)
    if length == 1: return [[1]]
    _returnM = []
    for i in range(length):
        _tmpList = []
        _returnM.append(_tmpList)
        for j in range(length):
            _M = copy.deepcopy(M)
            _M = [
                _l for _l in _M
                if _M.index(_l) != i
            ]
            [ _l.pop(j) for _l in _M ]
            _Determinant = getDeterminant(_M)
            _tmpList.append(((-1)**(i+j))*_Determinant)
    return Matrix(transpose(_returnM))

# 逆矩阵
def getInversedMatrix(M):
    # A* / |A|
    _Determinant = getDeterminant(M)
    k = 1/_Determinant
    _AdjugateMatrix = getAdjugateMatrix(M)
    # print(_AdjugateMatrix)
    _returnM = multiplyNumber(k, _AdjugateMatrix)
    return _returnM

def getProMatrix(M):
    pro_matrix = []
    ter_index = []
    run_index = []
    for index, l in enumerate(M):
        new_row = []
        if sum(l) > 0:
            run_index.append(index)
            for i in l:
                new_row.append(Fraction(i, sum(l)))
            pro_matrix.append(new_row)
        else:
            ter_index.append(index)
    return (pro_matrix, run_index, ter_index)
def f(x): return x > 0
def lcm(x, y): return (x.denominator * y.denominator / gcd(x.denominator, y.denominator))
def lcm_z(x, y): return (x * y / gcd(x, y))

def answer(m):
    if(len(m) == 0):
        return []
    elif(len(m) == 1):
        return [1, 1]
    else:
        # return [1, 1]
        pro_matrix, run_index, ter_index = getProMatrix(m)
        # print(pro_matrix)
        Q = [[pro_matrix[i][j] for j in ((run_index))] for i in range(len(run_index))]
        I = [[1 if i == j else 0 for i in range(len(run_index))] for j in range(len(run_index))]
        # print(Q)
        # print(I)
        R = [[pro_matrix[i][j] for j in ter_index] for i in range(len(run_index))]

        IQ = ([[I[i][j] - Q[i][j] for j in range(len(I[0]))] for i in range(len(I))])
        # print('---------')
        # print(IQ)
        F = getInversedMatrix(Matrix(IQ))

        # print(F)
        # print('---------')
        # print(R)
        if len(F) == 1 and len(R) == 1:
            return []
            # ret = F * R
        elif len(F) == 1:
            ret = multiplyNumber(F, Matrix(R))
        elif len(R) == 1:
            ret = multiplyNumber(R, Matrix(F))
        else:
            ret = multiplyMatrix(Matrix(F), Matrix(R))

        x = ret[0][0]
        y = ret[0][1]
        # print(x.denominator * y.denominator / gcd(x.denominator, y.denominator))



        # print(ret[0])
        # print(filter(f, ret[0]))
        # print(ret[0][0].denominator)
        # print(ret[0][1].denominator)
        # print ret[0][0].denominator * ret[0][1].denominator / gcd(ret[0][0].denominator, ret[0][1].denominator)
        # print(lcm(ret[0][0], ret[0][1]))
        temp = filter(f, ret[0])
        # print(temp)
        lcm_ret = 1
        for i in temp:
            lcm_ret = lcm_z(lcm_ret, i.denominator)
        # print(lcm_ret)
        kk = []
        for x in ret[0]:
            kk.append(lcm_ret / x.denominator * x.numerator)
        kk.append(lcm_ret)
        # print kk
        return kk
    # return kk
    # print(lcm_ret * ret[0])
    # print(ret[0] * lcm_ret)
    # min_i = min(filter(f, ret[0]))
    # for i in range(len(ret[0])):
    #     ret[0][i] = Fraction(Decimal(ret[0][i] / min_i))


    # print(ret[0])
    # print Fraction(Decimal(ret[0][1] / ret[0][2]))
    # print(sum(ret[0]))
    # Fraction(f).limit_denominator(ret[0][1])

if __name__ == "__main__":
    assert (
    answer([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
    )
    assert(answer([]) == [])
    assert (
        answer([
            [0, 1, 0, 0, 0, 1],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]) == [0, 3, 2, 9, 14]
    )

    assert (
        answer([
            [1, 2, 3, 0, 0, 0],
            [4, 5, 6, 0, 0, 0],
            [7, 8, 9, 1, 0, 0],
            [0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]) == [1, 2, 3]
    )
    assert (
        answer([
            [0]
        ]) == [1, 1]
    )



    assert (
        answer([
            [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
            [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
            [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
            [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
            [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [4, 5, 5, 4, 2, 20]
    )

    assert (
        answer([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [1, 1, 1, 1, 1, 5]
    )


    assert (
        answer([
            [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
            [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [6, 44, 4, 11, 22, 13, 100]
    )

    assert (
        answer([
            [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
            [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
            [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
            [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [1, 1, 1, 2, 5]
    )

    assert (
        answer([
            [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
            [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
            [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
            [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [1, 2, 3, 4, 5, 15]
    )

    assert (
        answer([
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]) == [2, 1, 1, 1, 1, 6]
    )
