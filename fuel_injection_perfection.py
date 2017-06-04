#!/usr/bin/env python
# encoding: utf-8

def answer2(n):
    dp = {}
    for i in range(n + 1):
        if i == 1:
            dp[i] = 0
        elif i == 0:
            dp[i] = 1
        else:
            if i % 2 == 0:
               dp[i] = dp[i / 2] + 1
            else:
                dp[i] = min(dp[i - 1], dp[(i + 1) / 2] + 1) + 1
    return dp[n]


def answer(n):
	n = long(n)
	if n == 0:
	    return 1
	ret = 0
	while n > 1:
		if n == 3:
			n = 1
			ret += 2
		elif n % 2 == 0:
			n /= 2
			ret += 1
		elif n % 4 == 1:
			n = n >> 1
			ret += 2
		else:
			n += 1
			ret += 1

	return ret

if __name__ == "__main__":
    print answer('4')
    print answer('2')
    print answer('3')

    print answer('15')
    print answer('3247923572983457289573458627345678229038409231852834578234965234756324875623459829034689042367834287568972543905890358904686834754839567347982562745627348564237856537826527865872435942369804328690438')
