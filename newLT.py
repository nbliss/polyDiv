class monomialOrdering(object):
	"""
	Object to compute the leading term based on a monomial ordering. 
	Sympy already has the option of computing leading term based on
	lex, grlex, grevlex, and elimination order, so if you're going to
	use one of those orderings just stick with sympy's, as it's much
	more efficient (monomials are ordered at time of polynomial creation.
	I've added support for lex, grlex, and grevlex for convenience, but
	the primary purpose of this class is for doing weighted ordering.
	"""
	from sympy import Poly,S
	def __init__(self,variables,ordering='lex',weightVector=(1,1,1)):
		"""
		Checks that the ordering is one of the ones we can deal with.
		Requires the sympy variables to be passed through (as a list)
		so LT can return an actual sympy polynomial (which needs the
		variables in its initialization)
		"""
		assert (ordering in ['lex','grlex','grevlex','weighted'])
		self.variables = variables
		self.ordering = ordering
		self.nv = len(variables)
		self.wv = weightVector

	def LT(self,poly):
		from sympy import Poly
		poly = Poly(poly,self.variables)
		polyDict = poly.as_dict()
		exponents = polyDict.keys()
		largest = exponents[0]
		for i in xrange(len(polyDict)):
			if self.compare(exponents[i],largest): largest = exponents[i]
		return Poly({largest:polyDict[largest]},self.variables)
		
	def LM(self,poly):
		from sympy import S,Poly
		poly = Poly(poly,self.variables)
		polyDict = poly.as_dict()
		exponents = polyDict.keys()
		largest = exponents[0]
		for i in xrange(len(polyDict)):
			if self.compare(exponents[i],largest): largest = exponents[i]
		return Poly({largest:S(1)},self.variables)

	def compare(self,monA,monB,lex=False):
		"""
		Based on monomial ordering, returns True if first is greater, False otherwise
		"""
		
		if self.ordering=='lex' or lex==True:
			for i in xrange(self.nv):
				if monA[i]>monB[i]:
					return True
				elif monA[i]<monB[i]:
					return False
				else: continue
			return True
		elif self.ordering=='grlex':
			sumA,sumB = sum(monA),sum(monB)
			if sumA==sumB:
				return self.compare(monA,monB,lex=True)
			elif sumA>sumB: return True
			else: return False
		elif self.ordering=='grevlex':
			sumA,sumB = sum(monA),sum(monB)
			if sumA==sumB:
				for i in xrange(self.nv):
					if monA[self.nv-i-1]>monB[self.nv-i-1]:
						return False
					elif monA[self.nv-i-1]<monB[self.nv-i-1]:
						return True
					else: continue
				return True
			elif sumA>sumB: return True
			else: return False
		else:
			assert self.ordering=='weighted'
			dotA = sum(monA[i]*self.wv[i] for i in xrange(self.nv)) 
			dotB = sum(monB[i]*self.wv[i] for i in xrange(self.nv)) 
			if dotA>dotB: return True
			elif dotA<dotB: return False
			else: return self.compare(monA,monB,lex=True)

if __name__=="__main__":
	from sympy import symbols,Poly
	x,y,z = symbols('x,y,z')
	symbolList = [x,y,z]
	mono = monomialOrdering(symbolList,ordering='lex')
	p = Poly(3*x*y**2-2*x*z+1)
	print p
	print mono.LT(p)
