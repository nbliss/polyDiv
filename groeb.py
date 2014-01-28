from sympy import *
x = symbols('x')
y = symbols('y')
z = symbols('z')
f = [x**2+1,x*y-1]

def groebnerBasis(f
	g = f
	h = 0
	while(g != h):
	    h = list(g)
	    for S in subsets(f,2):
		if S[0] != S[1]:
		    Spoly = ((lcm(LM(S[0]),LM(S[1]))/LT(S[0]))*S[0] - (lcm(LM(S[0]),LM(S[1]))/LT(S[1]))*S[1]).expand()
		    r = Spoly
		    k = 0
		    #From here to the next "#" I just threw in the code from lec4
		    while(r!=0 and k!= -1):
			k = -1
			for i in range(len(f)):
			    #If there's no common root(x+y, x**2 - 1, y**2 - 2*x), then it dies at the line below. I think what it is that kills it is that it gets an r value which is an integer. If r is an int, does that always mean that it's going to have a common root?
			    if div(LT(r),LT(f[i]))[1] == 0:
				k = i
				break
			if k!=-1:
			    r = (r - div(LT(r),LT(f[i]))[0]*f[k]).expand()
		    #

		if r!= 0:
		    g.append(Spoly)
	print "Groebner basis below:"
	print g

#So the above is a direct implementation of the algorithm. It works. Below, I've tried to add a way to get the reduced groebner basis. It might work..? It works sometimes, that's for sure.


for p in g:
    testg = list(g)
    del testg[testg.index(p)]
    r = p
    k = 0
    while(r!=0 and k!= -1):
        k = -1
        for i in range(len(testg)):
            if div(LT(r),LT(testg[i]))[1] == 0:
                k = i
                break
        if k!=-1:
            r = (r - div(LT(r),LT(testg[i]))[0]*testg[k]).expand()
    if(r == 0):
        g = list(testg)

for k in g:
    if(k.coeff(LM(k)) != 1):
        g[g.index(k)] = k/(k.coeff(LM(k)))

print "Reduced Groebner basis might be below:"
print g
