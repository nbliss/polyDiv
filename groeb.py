from sympy import *
from newLT import *
import sympy
x = symbols('x')
y = symbols('y')
z = symbols('z')
f = [Poly(x**2+1),Poly(x*y-1)]
s = [x,y]
f = [Poly(x**2+1,s,domain='QQ'),Poly(x*y-1,s,domain='QQ')]

def groebasis(f,s):
	from newLT import *
        mono = monomialOrdering(s,ordering='lex')
	g = f
	h = 0
	while(g != h):
		h = list(g)
		for S in subsets(f,2):
			if S[0] != S[1]:
				AA = lcm(mono.LM(S[0]),mono.LM(S[1]))/mono.LT(S[0])
				BB = lcm(mono.LM(S[0]),mono.LM(S[1]))/mono.LT(S[1])
				if type(AA) != Poly:
					AA = Poly(AA,s,domain='QQ')
				if type(BB) != Poly:
					BB = Poly(BB,s,domain='QQ')
				Spoly = AA*S[0] - BB*S[1]
				r = Spoly
				k = 0
			 	while(r!=0 and k!= -1):
			        	k = -1
			        	for i in range(len(f)):
			         #If there's no common root(x+y, x**2 - 1, y**2 - 2*x), then it dies at the line below. I think what it is that kills it is that it gets an r value which is an integer. If r is an int, does that always mean that it's going to have a common root?
			         		if div(mono.LT(r),mono.LT(f[i]))[1] == 0:
			               			k = i
			                		break
			        	if k!=-1:
			        		r = (r - div(mono.LT(r),mono.LT(f[i]))[0]*f[k]).expand()
			if r!= 0:
				g.append(Spoly)
	print "Groebner basis below:"
	print g

	#http://www.kent.ac.uk/smsas/personal/gdb/MA574/week6.pdf
	#The above algorithm is implemented below. First, getting a minimal groebner basis:

	monicg = []
	for k in g:
		leadingCoeff = mono.LT(k).as_dict().values()[0]
		monicg.append(Poly(k/leadingCoeff,s,domain='QQ'))


	H2 = [] #Using notation of kent algorithm
	minimalg = []
	for k in monicg:
		if mono.LT(k) not in H2:
			H2.append(mono.LT(k))
			minimalg.append(k)
	print "Minimal Groebner basis below:"
	print minimalg

	holdd = len(minimalg)
	for ka in range(holdd):
		r = minimalg.pop(0)
		k = 0
	 	while(r!=0 and k!= -1):
	        	k = -1
	        	for i in range(len(minimalg)):
	         		if div(mono.LT(r),mono.LT(minimalg[i]))[1] == 0:
	               			k = i
	                		break
	        	if k!=-1:
	        		r = (r - div(mono.LT(r),mono.LT(minimalg[i]))[0]*minimalg[k]).expand()
		if r != 0:
			minimalg.append(r)

	print "Reduced Groebner basis below:"
	print minimalg


	return



if __name__=="__main__":
	groebasis(f,s)
