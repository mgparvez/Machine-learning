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

    
def bag(tdata):                         #function for bagging
    subset=[]
    n=len(tdata)
    while len(subset)<n:
        subset.append(tdata[rd.randrange(n)])
    return subset
def predict(xin,theta):
    prob=sig(mul([xin],theta))
    if prob[0][0]>=0.5:
        return("1")
    else:
        return("0")    
    
        
#----------------------------------------------------Training-----------------------------------------------------------------
tdata=[]
datat=[]

f= open('train','rt')                                                      #opening the train data file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
f= open('test','rt')                                                      #opening the  test data file

try:
    for line in f:
        line=line.rstrip('\n')
        datat.append(line.split(','))
finally:
    f.close()
#avg_theta=[[0.000 for i in range(1)] for j in range(len(tdata[0])-1)]
avg=[]
n=input("Enter number of times to do bagging\n")
for i in range(n):
    t=logi(bag(tdata))
    avg.append(t)
    #avg_theta=[[(avg_theta[j][i]+t[j][i]) for i in range(1)]for j in range(len(tdata[0])-1)]
#avg_theta=[[(avg_theta[j][i]/n) for i in range(1)]for j in range(len(tdata[0])-1)]
acc=[0]
er=0.0                     
i=0
y=[]
prob=0.0
for d in tdata:
    for i in range(len(avg)):
        t=avg[i]
        t=sig(mul([map(float,d[:(len(d))])],t))
        prob+=t[0][0]
    prob=prob/len(avg)
    if prob>=0.5:
        y.append(1)
    else:
        y.append(0)
    if(y[len(y)-1]!=int(d[len(d)-1])):
        er+=1
print "train prediction",y
print("train error",(er/len(tdata)))

er=0.0                      
i=0
y=[]
prob=0.0
for d in datat:
    for i in range(len(avg)):
        t=avg[i]
        t=sig(mul([map(float,d[:(len(d))])],t))
        prob+=t[0][0]
    prob=prob/len(avg)
    if prob>=0.5:
        y.append(1)
    else:
        y.append(0)
    if(y[len(y)-1]!=int(d[len(d)-1])):
        er+=1
print "test prediction",y
print("testing error",(er/len(datat)))
  
    

