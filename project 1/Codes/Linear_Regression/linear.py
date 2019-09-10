
#----------------------------------------------Basic matrix operations----------------------------------------------
def mul(x,y):
    r=[[0 for i in range(len(y[0]))] for j in range(len(x))]
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                r[i][j] +=x[i][k]*y[k][j]
    return r


def prin(x):
    for r in x:
        print r
def trans(m):
    return map(list,zip(*m))

def minor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def det(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*det(minor(m,0,c))
    return determinant

def inverse(m):
    determinant = det(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minr = minor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * det(minr))
        cofactors.append(cofactorRow)
    cofactors = trans(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors




#----------------------------------------------------Training------------------------------------------

tdata=[]

f= open('data','rt')                                                      #opening the data file

try:
    for line in f:
        line=line.rstrip('\n')
        
        tdata.append(map(float,line.split(',')))
finally:
    f.close()
#print tdata
x=[]
y=[]
for d in tdata:
    x.append(d[0:2])                                            #extracting input and output values from the data
    y.append(d[2])
print len(x)
#print x
#deg=3
deg=input("enter the order\n")                                 #order of polynomial
n=int(.5*(deg+2)*(deg+1))

matx=[[0 for i in range(n)] for j in range(len(x))]            #defining x  feature matrix
maty=[[0 for i in range(1)] for j in range(len(x))]            #defining y matrix



for s in range(len(x)):                                        #generating the features of x
    #print s
    k=0
    for i in range(deg+1):
        for j in range(deg+1-i):
            matx[s][k]=pow(x[s][0],j)*pow(x[s][1],i)
            #print k
            k=k+1
for s in range(len(x)):
    maty[s][0]=y[s]
    
tmatx=trans(matx)                                              #x matrixx transpose
pseudoinv=mul(inverse(mul(tmatx,matx)),tmatx)                  # calculating the moore-penrose pseudoinverse
theta=mul(pseudoinv,maty)                                      #getting theta =pseudoinverse*Y
print "Theta:"
prin(theta)

#--------------------------------------------------------Testing-------------------------------------------------

testdata=[]
f= open('test','rt')                                                      #opening the test file
try:
    for line in f:
        line=line.rstrip('\n')
        
        testdata.append(map(float,line.split(',')))
finally:
    f.close()
tx=[]
ty=[]
for d in testdata:
    tx.append(d[0:2])
    ty.append(d[2])
print len(x)
#print x

tmatx=[[0 for i in range(n)] for j in range(len(tx))]
tmaty=[[0 for i in range(1)] for j in range(len(tx))]
for s in range(len(tx)):
    #print s
    k=0
    for i in range(deg+1):
        for j in range(deg+1-i):
            tmatx[s][k]=pow(tx[s][0],j)*pow(tx[s][1],i)
            #print k
            k=k+1
for s in range(len(tx)):
    tmaty[s][0]=ty[s]



h=mul(tmatx,theta)                                                         #commputing hypthesis = X*theta
su=0
for i,j in zip(h,tmaty):                                                #calculating RMS error between hypothesis and test output y
    su+=pow((i[0]-j[0]),2)
err=pow((su/len(h)),.5)

print "The error is:",err                                                               #Printing Error

