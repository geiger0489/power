# power
My implementation of power(b, e). 
It takes any real b and e and returns b^e.

Exceptions:
  if b == 0 and e == 0 it raises an exception because 0^0 is undefined value.
  if b == 0 and e < 0 it raises "division by zero" exception.
  if b < 0 and e is uneven it raises exception because the result is undefined (it doesn't work with complex numbers).
  
For evaluating b^e where e is fraction I use Newton's iteration algorhytm.

Also when e is a fraction (e.g. 2^1.25) it's the same as 2*2^0,25 = 2*2^(1/4).
So to get this fraction (1/4) I use simplification algorhytm.

It works as follows:
1. Given 2^1.25
2. 1.25 = 1 + 0.25
3. 0.25 = 25/100
4. 25/100 = 5*5/5*5*2*2 = 1/2*2 = 1/4 - represented as a tuple (1,4)

Now power function works really slow. Hope to find a way to make it faster.
