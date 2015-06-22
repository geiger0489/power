PRECISION = 1e-12 #decimal places

def taylor_sin(x):
    '''
    Calculates sin(x), where sin(x) is represented
    as taylor's series (n-th sum of terms).
    The higher n you take the more precise result you get.
    '''

    r, i = 0, 0
    delta = x #start value
    
    while abs(delta) > PRECISION:
        delta = power(-1, i) / factorial(2*i+1) * power(x, 2*i+1)  
        r += delta
        i += 1
    return r

def taylor_cos(x):
    '''
    Calculates cos(x), where cos(x) is represented
    as taylor's series (n-th sum of terms).
    The higher n you take the more precise result you get.
    '''

    r, i = 0, 0
    delta = x #start value
    
    while abs(delta) > PRECISION:
        delta = power(-1, i) / factorial(2*i) * power(x, 2*i)  
        r += delta
        i += 1
    return r

def taylor_asin(x):
    '''
    Calculates arcsin(x), where arcsin(x) is represented
    as taylor's series (n-th sum of terms).
    The higher n you take the more precise result you get.
    '''
    
    if abs(x) >= 1:
        raise ValueError('arcsin(x) is defined for |x| < 1.')
    
    r, i = 0, 0
    delta = x #start value
    
    while abs(delta) > PRECISION: # maximum precision possible without overflow
        #first two numbers are very big
        #so big, that I get overflow error
        #that's why I use int arithmetics
        delta = factorial(2*i) // power(factorial(i), 2) \
                / (power(4, i) * (2*i+1)) * power(x, 2*i+1) 
        r += delta                                          
        i += 1
    return r
    
def factorial(n):
    '''
    Calculates n! = 1*2*3*4...*n
    '''
    
    f = 1
    for i in range(n):
        f = f * (i + 1)
    return f

def factorize(a):
    '''
    Factorizes a given number returning a list of coefficients.
    e.g factorize(10) = [1, 2, 5], factorize(-10) = [-1, 2, 5].
    Input parameter should be an integer number.
    '''
    
    if a % 1:
        raise TypeError('Trying to factorize non integer number.')
    if not a:
        return [0]
    m = [a/abs(a),]
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
    and returns a tuple containig two numbers (a, b),
    so that a/b = m, and a/b is the simplified ratio.
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
    calculate approximate value of e-th root of b.
    For uneven e, b can have any Real value.
    In case of even e, b should be non negative. 
    Exponent e should always be > 0.
    '''
    
    if b == 0:
        return 0
        
    if b < 0:
        if e % 2:
            return -1 * newton_root(-b, e)
        else:
            raise Exception('trying to evaluate root of even degree from a negative number.')
        
    r = 1
    delta = 1
    while abs(delta) > PRECISION:
        delta = 1 / e * (b / power(r, e - 1) - r )
        r += delta   
    return r

def power(b, e):
    '''
    Function returning b^e where 
    b - base and e - exponent
    works for Real b and e.
    Expected to work with Complex b and e in future.
    '''
    
    # exceptions
    if b == e == 0:
        raise ValueError('0^0 is not defined.')
        
    if b == 0 and e < 0:
        raise ValueError('1/0 is not defined.')
    
    if b == 0 and e > 0:
        return 0
        
    if e < 0:
        return 1 / power(b, -e)
        
    if not e % 1: #for integer e
        n = 1
        for i in range(e):
            n = n * b
        return n
        
    else: #for fractional e
        f = e % 1 #fractional part
        c = round(e - f) #integer part
        f = simplify(f)
        # e.g. 2^0,5 = 2^(5/10) = 2^(5/5*2) = 2^(1/2) = (2^1)*sqrt(2)
        return power(b, c) * newton_root( power(b, f[0]), f[1] )

def complex_power(b, e):
    '''
    Function returning b^e where 
    b and/or e are complex (x+yj).
    (a+bj)^n = r^n * (cos(n*phi) + jsin(n*phi))
    where phi = Arg(a+bj) = arccos(b/sqrt(a^2 + b^2))
    '''
    '''
    c = (b.real, b.imag)
    r = newton_root(c[0]*c[0] + c[1]*c[1], 2)
    return c, r'''
 
if __name__ == '__main__':
    import unittest
    
    #=========================================================================
    class FactorizationTestCase(unittest.TestCase):
        
        def test_factorize_for_numbers_from_minus_1000_to_1000(self):
            for i in range(-1000, 1000):
                f = factorize(i)
                n = 1
                for j in f:
                    n = n * j
                self.assertEqual(n, i)
    
    #=========================================================================
    class SimplificationTestCase(unittest.TestCase):
        
        def test_simplify_for_numbers_from_0_001_to_1(self):
            total = 1000
            for i in range(total):
                _in = i / total
                _out = simplify(i / total)
                _out = _out[0] / _out[1]
                self.assertEqual(_in, _out)
    
    #=========================================================================    
    class NewtonRootTestCase(unittest.TestCase):
    
        def test_7th_newton_root_for_numbers_from_minus_0_to_1000(self):
            for i in range(1000):
                r = newton_root(i, 7)
                self.assertTrue(abs(r - pow(i, 1/7)) <= PRECISION)

    #=========================================================================    
    class FactorialTestCase(unittest.TestCase):
    
        def test_factorial_for_i_in_range_0_to_100(self):
            from math import factorial as fact
            for i in range(100):
                self.assertEqual(factorial(i), fact(i))

    #=========================================================================    
    class TaylorSinTestCase(unittest.TestCase):
    
        def test_taylor_sin_for_i_in_range_0_to_2pi(self):
            from math import sin
            for i in range(1, 1000):
                n = 6.28 / i
                self.assertTrue(abs(taylor_sin(n) - sin(n)) <= PRECISION)
    
    #=========================================================================    
    class TaylorCosTestCase(unittest.TestCase):
    
        def test_taylor_cos_for_i_in_range_0_to_2pi(self):
            from math import cos
            for i in range(1, 1000):
                n = 6.28 / i
                self.assertTrue(abs(taylor_cos(n) - cos(n)) <= PRECISION)

    #=========================================================================    
    class TaylorAsinTestCase(unittest.TestCase):
    
        def test_taylor_asin_for_i_in_range_min_1_to_1(self):
            from math import asin
            for i in range(-9999, -1):
                n = 1 / i
                self.assertTrue(abs(taylor_asin(n) - asin(n)) <= PRECISION)
            for i in range(2, 9999):
                n = 1 / i
                self.assertTrue(abs(taylor_asin(n) - asin(n)) <= PRECISION)
            self.assertTrue(taylor_asin(0) == 0)
                
    #=========================================================================
    class PowerTestCase(unittest.TestCase):
    
        def test_power_for_b_in_0_to_1_and_e_in_0_to_1(self):
            for i in range(1, 100):
                b = e = i / 100
                p = power(b, e)
                self.assertTrue(abs(p - pow(b, e)) <= PRECISION)
                
        def test_power_for_b_in_1_to_1000_and_e_equals_to_3(self):
            for i in range(1, 1000):
                p = power(i, 5)
                self.assertTrue(abs(p - pow(i, 5)) < PRECISION)
        
        def test_power_for_negative_b_and_uneven_positive_e(self):
            self.assertEqual(power(-3, 5), pow(-3, 5))
                
        def test_power_for_negative_b_and_uneven_negative_e(self):
            self.assertEqual(power(-3, -5), pow(-3, -5))

        def test_power_for_negative_b_and_even_positive_e(self):
            self.assertEqual(power(-3, 4), pow(-3, 4))
                
        def test_power_for_negative_b_and_even_negative_e(self):
            self.assertEqual(power(-3, -4), pow(-3, -4))
            
    #=========================================================================            
    
    #start testing
    unittest.main()
