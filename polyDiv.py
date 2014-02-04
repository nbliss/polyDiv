def polyDiv(p,L):
	"""
	Accepts a polynomial p and a list of polynomials L.
	Returns the remainder after division of p by L.
	Input should by sympy polynomials.:
	"""
	from sympy import symbols,Poly,LT,div
	print type(LT(p))
	print type(p)
	print p
	r = p
	k = 0
	while(r!=0 and k!= -1):
	    k = -1
	    for i in range(len(L)):
		if div(Poly(LT(r)),LT(Poly(L[i])))[1] == 0:
		    k = i
		    break
	    if k!=-1:
		r = (r - div(Poly(LT(r)),Poly(LT(L[i])))[0]*L[k]).expand()
	return r

if __name__=="__main__":
	from sympy import symbols,Poly
	x = symbols('x')
	y = symbols('y')
	L =  [Poly(3*x + y), Poly(y**2 + 3)]
	p = Poly(x*y-1)
	print type(p)
	print polyDiv(p,L)
