import math as m
import random as rd

#-----------------------------------------------Basic matrix operations---------------------
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


def sub(a,b):
    s=a
    for i in range(len(s)):
        for j in range(len(s[0])):
            s[i][j]=a[i][j]-b[i][j]
    return(s)


    
#----------------------------------------------------Sigmoid and Gradient functions------------------------

def sig(a):                                                        #Function for Sigmoid
    s=a
    for i in range(len(s)):
        for j in range(len(s[0])):
            s[i][j]=1/(1+m.exp(-s[i][j]))
    return(s)

def gradient(x,h,y,a):                                              #function for Gradient calculation
    
    diff=(sub(h,y))
    grd=mul(trans(x),diff) 
    for i in range(len(grd)):
        for j in range(len(grd[0])):
            grd[i][j]=a*grd[i][j]                          #gradient= xT*(H-Y)
    
    return(grd)
def logi(tdata):
    itr=100
    alpha=0.01
    x=[]
    y=[]
    for d in tdata:
        x.append(map(float,d[:(len(d)-1)]))                                  #Extracting features from data and storing in x
        if d[len(d)-1]=='1':                                                #Assingning values to class (M=1,W=0)
            y.append([1])
        else:
            y.append([0])
    theta=[[0 for i in range(1)] for j in range(len(x[0]))]
    i=0
    while i<itr:
        theta_prev=theta
        h=sig(mul(x,theta))
        #prin(y)
        #diff=(sub(h,y))
        grd=gradient(x,h,y,alpha)
        #prin(grd)
        theta=sub(theta,grd)
        i+=1
    return(theta)


    
def bag(tdata,w):
    subset=[]
    n=len(tdata)
    while len(subset)<n:
        r=rd.randrange(10000)/10000.0
        i=0
        c=0
        while(c+w[i]<r and i<len(w)-1):
            i+=1
            c=c+w[i]
        subset.append(tdata[i])
    return subset
def predict(xin,theta):
    prob=sig(mul([xin],theta))
    if prob[0][0]>=0.5:
        return("1")
    else:
        return("0")    
    
        
#----------------------------------------------------Training-----------------------------------------------------------------
tdata=[]

f= open('train','rt')                                                      #opening the data file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
    n=len(tdata[0])
wt=[(1.00/len(tdata)) for i in range(len(tdata))]
avg_theta=[[0.000 for i in range(1)] for j in range(len(tdata[0])-1)]
k=input("Enter number of times to apply boosting\n")
model=[]
er=0.0
alpha=[]
first =True
for i in range(k):
    if(first):
        t=logi(tdata)
        first = False
    else:
        t=logi(bag(tdata,wt))
    for d in tdata:
        if(predict(map(float,d[:(n-1)]),t)!=d[n-1]):
            er+=wt[i]
    er=er/sum(wt)
    if er<0.5:
        alpha.append(0.5*m.log((1-er)/er))
        model.append(t)
        for j in range(len(wt)):
            wt[j]=wt[j]*m.exp(-alpha[i]*(2*int(tdata[j][n-1])-1)*(2*int(predict(map(float,tdata[j][:n-1]),model[i]))-1))

hx=[]
h=0.0
for d in tdata:
    h=0.0
    for i in range(len(alpha)):
        h+=alpha[i]*(int(predict(map(float,d[:n-1]),model[i]))-(1-int(predict(map(float,d[:n-1]),model[i]))))
    if(1/(1+m.exp(-h))>=0.5):
        hx.append(1)
    else:
        hx.append(0)
print "train prediction", hx

er=0.0
for i in range(len(hx)):
    if(hx[i]!=int(tdata[i][n-1])):
        er+=1
er=er/len(hx)
print "training error",er

tdata=[]
hx=[]
f= open('test','rt')                                                      #opening the test data file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
    n=len(tdata[0])
for d in tdata:
    h=0.0
    for i in range(len(alpha)):
        h+=alpha[i]*(int(predict(map(float,d[:n]),model[i]))-(1-int(predict(map(float,d[:n]),model[i]))))
    if(1/(1+m.exp(-h))>=0.5):
        hx.append(1)
    else:
        hx.append(0)
print "test prediction",hx
er=0.0
for i in range(len(hx)):
    if(hx[i]!=int(tdata[i][n-1])):
        er+=1
er=er/len(hx)
print "testing error",er


