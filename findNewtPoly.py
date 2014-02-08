import newLT
from sympy import symbols,Poly
x,y = symbols('x,y')
symbolList = [x,y]
p = Poly(y**4+1+x**4+x**4*y**2+x**3*y**3+y+y**2+y**3+x*y+x**2*y+x*y**2+x**2*y**2+x*y**3+x**4*y)
ltFunct = lambda v:newLT.monomialOrdering(symbolList,ordering='weighted',weightVector=v).LT(p)
vertices = []
for i in xrange(40):
	for j in xrange(40):
		for sgn in [(1,1),(-1,1),(1,-1),(-1,-1)]:
			newguy = ltFunct((sgn[0]*i/40.0,sgn[1]*j/39.0))
			if newguy not in vertices: 
				vertices.append(newguy)
for vertex in vertices:
	print vertex.as_expr()
