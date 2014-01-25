from sympy import *
x = symbols('x')
y = symbols('y')
L = [y*y-1,x*y+1]
p = x*y*y-x


r = p
k = 0
while(r!=0 and k!= -1):
    k = -1
    for i in range(len(L)):
        if div(LT(r),LT(L[i]))[1] == 0:
            k = i
            break
    if k!=-1:
        r = (r - div(LT(r),LT(L[i]))[0]*L[k]).expand()
print r