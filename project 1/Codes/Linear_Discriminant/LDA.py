import math
#--------------------------------------------------------Basic matrix operations-----------------------------------------------
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



def sub(a,b):
    s=a
    for i in range(len(s)):
        for j in range(len(s[0])):
            s[i][j]=a[i][j]-b[i][j]
    return s
def add(a,b):
    s=a
    for i in range(len(s)):
        for j in range(len(s[0])):
            s[i][j]=a[i][j]+b[i][j]
    return s

#--------------------------------------------------------Training---------------------------------------------------------------

def train(x,y):                                         #function to Train the model.
    y1=0
    y0=0
    temp1=[0]*len(x[0])
    temp0=[0]*len(x[0])
    k=0
    for d in y:                                
        if d[0]==1:
            y1=y1+1
            for i in range(len(x[0])):
                temp1[i]=temp1[i]+x[k][i]
        else:
            y0=y0+1
            for i in range(len(x[0])):
                temp0[i]=temp0[i]+x[k][i]
        k+=1
            
            

    py1=(float(y1))/(len(y))                 #probability of a given class=1
    py0=(float(y0))/(len(y))                 #probability of a given class=1
    mean1=[0]*len(x[0])
    mean0=[0]*len(x[0])
    for i in range(len(x[0])):               #calculating the means for each attribute
        mean1[i]=[float(temp1[i])/y1]
        mean0[i]=[float(temp0[i])/y0]
    #print y1,y0,mean1,mean0
    
    cov=[[0 for i in range(len(x[0]))] for j in range(len(x[0]))]   #calculating covariance matrix
    for k in range(len(x)):                                                 
        te=[]
        for i in range(len(x[0])):
            if(y[k]==1):
                te.append([x[k][i]-mean1[i][0]])
            else:
                te.append([x[k][i]-mean0[i][0]])
        m=mul(te,trans(te))
        cov=add(cov,m)
    cov=[[(cov[j][i]/(len(x))) for i in range(len(x[0]))] for j in range(len(x[0]))]
    
    rhs=sub(mul(mul(trans(mean1),inverse(cov)),mean1),mul(mul(trans(mean0),inverse(cov)),mean0)) #calculating Right hand side of the boundary equation
    rhs[0][0]=rhs[0][0]/2-math.log(py1/py0)
    
    return(sub(mean1,mean0),cov,rhs)




tdata=[]

f= open('data','rt')                                                      #opening the file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
x=[]
y=[]
for d in tdata:
    x.append(map(float,d[:(len(d)-1)]))                             #Extracting features (h,w,a) from data and storing in x
    if d[len(d)-1]=='M':                                                #Assingning values to class (M=1,W=0)
        y.append([1])
    else:
        y.append([0])                    
    
#print len(x)

diff_mean,covariance,rhs=train(x,y)
#print diff_mean,"\n",covariance,"\n",rhs
#-----------------------------------------------Prediction---------------------------------------------------
inp=raw_input("enter height weight and age h,w,a\n")                #getting input for prediction
inp=inp.split(',')
inp=map(float,inp)
xin=[]
xin.append(inp)
print xin
lhs=mul(mul(trans(diff_mean),inverse(covariance)),trans(xin))      #computing LHS using the prediction data
cls=(1*(lhs[0][0]>rhs[0][0]))                                      #Checking the boundary condition
print "the class is:"
if cls:
    print "M"
else:
    print "W"



