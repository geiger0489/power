PRECISION = 1e-12 #decimal places

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
        n = 1.0
        for i in range(e):
            n = n * b
        return n
        
    else: #for fractional e
        f = e % 1 #fractional part
        c = round(e - f) #integer part
        f = simplify(f)
        return power(b, c) * newton_root( power(b, f[0]), f[1] )
        # e.g. 2^0,5 = 2^(5/10) = 2^(5/5*2) = 2^(1/2) = (2^1)*sqrt(2)

        
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
