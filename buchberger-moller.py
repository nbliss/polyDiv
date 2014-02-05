"""
Monomials are stored as single key dictionaries {vector tuple : coeff}
Polynomials are the same, just with multiple entries

"""

def buchMol(points,ordering,weightVector=(1,1,1)):
	"""
	Given X = [(c11,c12,...,c1n),...,(cs1,cs2,...,csn)] affine point set
	and ordering 'lex','grlex','grevlex', or 'weighted' (plus a weight vector)
	computes reduced Groebner basis and Q-basis of the ring mod the ideal
	"""
	from sympy import symbols,Poly,div,Rational,Matrix
	from newLT import monomialOrdering
	dim = len(points[0])
	for pt in points:   # check that all pts have same dimension
		assert len(pt)==dim
	if dim in [1,2,3]:
		l = ['x','x,y','x,y,z']
		varlist = symbols(l[dim-1])
	else:
		varstring = 'x0'
		for i in xrange(1,dim):
			varstring+=',x'+str(i)
		varlist = symbols(varstring)
	monClass = monomialOrdering(varlist,ordering,weightVector)
	counter = 0 # keep track of number of rows of matrix & size of S
	G,normalSet,S = [],[],[]
	L = [Poly(1,varlist,domain='QQ')] 
	M = Matrix(0,len(points),[])
	pivots = {} # {column:row}
	while L!= []:
		# step 2:
		t = L[0]
		for elmt in L:
			if monClass.compare(t.as_dict().keys()[0],elmt.as_dict().keys()[0]):
				t = elmt
		L.remove(t)
		evalVector = Matrix(1,len(points),[t.eval(pt) for pt in points])
		print "hi"
		print M
		print evalVector
		v,a = vecReduce(evalVector,M,pivots)
		print v
		viszero = False
		if firstNonzero(v)==-1: viszero = True
		toAdd = t
		for i in xrange(counter):
			toAdd +=Poly(-1,varlist)*Poly(a[i],varlist)*S[i] 
		if viszero:
			G.append(toAdd)
			for mon in L:
				if div(t,mon)[1]==0:
					L.remove(mon)
		else:
			pivSpot = firstNonzero(v)
			pivots[pivSpot]=M.shape[0]
			M = M.col_join(v)
			S.append(toAdd)
			counter+=1
			normalSet.append(t)
			for variable in varlist:
				toCheck = Poly(variable,varlist)*t
				isMultiple = False
				for elmt in L:
					if div(elmt,toCheck)[1]==0:
						isMultiple = True
						break
				if isMultiple: continue
				for elmt in G:
					if div(monClass.LT(elmt),toCheck)[1]==0:
						isMultiple = True
						break
				if isMultiple == False:
					L.append(toCheck)
	return G,normalSet

def vecReduce(vec,mat,pivots):
	"""
	Reduces the vector vec against the rows of mat to obtain
	a reduced vector v = (t(p1),..) - Sum(ai * mat[:,i])
	and returns the vector and the ai's
	Note: pivots is {column:row}
	"""
	from sympy import Rational
	a = {}
	if mat.shape[0]==0: return vec,a.values()
	toCheck = firstNonzero(vec)
	if toCheck == -1: return vec,a.values()
	while True:
		if toCheck in pivots:
			a_value = Rational(vec[toCheck])/Rational(mat[toCheck,pivots[toCheck]])
			vec -= a_value*mat[pivots[toCheck],:]
			a[pivots[toCheck]]=a_value
		else: break
		oldToCheck = toCheck
		for i in xrange(toCheck+1,mat.shape[1]):
			if vec[i]!=0:
				toCheck = i
				break
		if oldToCheck==toCheck: break
	for i in xrange(mat.shape[0]):
		if i not in a.keys():
			a[i]=0
	return vec,a.values()


def firstNonzero(vec):
	"""
	returns the index of the first nonzero entry in vec,
	or -1 if vec is all zeros
	"""
	for i in xrange(len(vec)):
		if vec[i]!=0: return i
	return -1

if __name__=="__main__":
	from sympy import S
#	points = [[0,0],[0,-1],[1,-2],[1,1],[-1,2]]
	points =[[0,0],[0,-1],[1,0],[1,1],[-1,1]] 	
	basis,normalSet = buchMol([[0,0],[0,-1],[1,0],[1,1],[-1,1]],ordering='grlex')	
	print "Basis:"
	for b in basis:
		print b.as_expr()
	print "Normal set:"
	for b in normalSet:
		print b.as_expr()
