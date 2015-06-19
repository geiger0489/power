PRECISION = 1e-12 #decimal places

def factorize(a):
	if not a: return [0]
	m = []
	a = abs(a)
	i = 2;
	while not a == 1:
		if a % i:
			i += 1
		else:
			m.append(i)
			a = a / i
	return m

def simplify(m):
    '''
    Takes 0<m<1 (e.g. 0,6527)
    and returns a tuple containig two numbers (a, b)
    so that a/b = m, and a/b is the simplified ratio
    '''
    
    # decimal places, denominator, numerator
    ln = len(str(m)) - 2
    den = power(10, ln)
    num = round(m * den)
    
    #factorization
    num_f = factorize(num)
    den_f = factorize(den)
    
    #simplification
    g = num_f if len(num_f) > len(den_f) else den_f
    s = num_f if g is den_f else den_f
    
    del_list = []
    j = 0
    
    for i in s:
        if i in g:
            g.remove(i)
            del_list.append(j)
        j += 1
    
    d = 0
    for i in del_list:
        del s[i - d]
        d += 1
    
    #assembling den and num
    num = 1
    for i in num_f:
        num = num * i
    
    den = 1
    for i in den_f:
        den = den * i
    
    return (num, den)

def newton_root(b, e):
    '''
    Implements Newton's method to 
    calculate approx value of e-th root from b
    e must be ceil and e != 0, 
    '''
    
    r = 1
    delta = 1
    while abs(delta) > PRECISION:
        delta = 1 / e * (b / power(r, e - 1) - r )
        r += delta   
    return r

def power(b, e):
    '''
    Function returns b^e where 
    b - base and e - exponent
    works for both Real and Complex b and e.
    e.g. both b^e and (a+bj)^(c+dj)
    '''
    
    # Exceptions
    if b == e == 0:
        raise Exception('0^0 is not defined.')
        
    if b == 0 and e < 0:
        raise Exception('1/0 is not defined.')
    
    if b == 0 and e > 0:
        return 0
        
    if e < 0:
        return 1 / power(b, -e)
    
    #For ceil e
    if not e % 1:
        n = 1.0
        for i in range(e):
            n = n * b
        return n
        
    #For fractional e
    else:
        f = e % 1 #fractional part
        c = round(e - f) #ceil part
        
        f = simplify(f)
        
        if b < 0 and not f[1] % 2:
            raise Exception('trying to get root of even degree from a negative number.')
        
        return power(b, c) * newton_root( power(b, f[0]), f[1] )
        
if __name__ == '__main__':
    import timeit

    # automated tests
    print('Running automate tests...\n')

    # factorization
    factorization_test_ok = True
    for i in range(1000):
        
        n = 1
        for j in factorize(i):
            n = n * j
            
        if not i == n:
            factorization_test_ok = False
            
    print('factorization_test_ok =', factorization_test_ok)
    print('Repeat 10000 times =', timeit.timeit('factorize(1000)',
                                 setup="from __main__ import factorize",
                                 number=10000), 'sec.\n')
    
    # simplification
    simplification_test_ok = True
    for i in range(1000):
 
        num = i / 1000
        s = simplify(num)
        
        if not s[0]/s[1] == num:
            simplification_test_ok = False
    
    print('simplification_test_ok =', simplification_test_ok)
    print('Repeat 10000 times =', timeit.timeit('simplify(0.2647)',
                                 setup="from __main__ import simplify",
                                 number=10000), 'sec.\n')

    # newton_root
    from math import pow
    
    newton_root_test_ok = True
    for i in range(1, 1000):

        r = newton_root(i, 7)
        
        if abs(r - pow(i, 1/7)) > PRECISION:
            newton_root_test_ok = False
    
    print('newton_root_test_ok =', newton_root_test_ok)
    print('Repeat 10000 times =', timeit.timeit('newton_root(2537, 18)',
                                 setup="from __main__ import newton_root",
                                 number=10000), 'sec.\n')
    
    # power
    power_test_ok = True
    for i in range(1, 100): # 0<b<1, 0<e<1
        base = expo = i / 100
        p = power(base, expo)
        
        if abs(p - pow(base, expo)) > PRECISION:
            power_test_ok = False
    
    
    for i in range(1, 1000): # 1<=b<10000, e=3
        
        p = power(i, 5)
        
        if abs(p - pow(i, 5)) > PRECISION:
            power_test_ok = False
            
    if not power(-3, 5) == pow(-3, 5):
        power_test_ok = False
        
    if not power(-3, -5) == pow(-3, -5):
        power_test_ok = False
   
    print('power_test_ok =', power_test_ok)
    print(power(12.02, 7.03))
    
    '''
    print('Repeat 1000 times =', timeit.timeit('power(12.678, 7.985)',
                                  setup="from __main__ import power",
                                  number=1), 'sec.\n')'''
    
    input('\nPress any key to exit...')
