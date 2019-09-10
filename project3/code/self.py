 
import random as rand
import math as m
import copy

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
            try:
                s[i][j]=float(1/(1+m.exp(-s[i][j])))
            except OverflowError:
                s[i][j]=1/float('inf')
    return(s)

def gradient(x,h,y,a):                                              #function for Gradient calculation
    
    diff=(sub(h,y))
    grd=mul(trans(x),diff) 
    for i in range(len(grd)):
        for j in range(len(grd[0])):
            grd[i][j]=a*grd[i][j]                          #gradient= xT*(H-Y)
    
    return(grd)
def logi(tdata):
    itr=300
    alpha=0.01
    x=[]
    y=[]
    for d in tdata:
        x.append(map(float,d[:(len(d)-1)]))                                  #Extracting features from data and storing in x
        if d[len(d)-1]=='M':                                                #Assingning values to class (M=1,W=0)
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
def predict(xin,theta):
    prob=sig(mul([xin],theta))
    return prob[0][0]
    '''if prob[0][0]>=0.5:
        return("1")
    else:
        return("0")'''   
    
    
data_u=[]
data_s=[]
data_stemp=[]
tdata=[]
f= open('data_u','rt')                                                      #opening the unlabelled data file

try:
    for line in f:
        line=line.rstrip('\n')
        data_u.append(map(float,line.split(',')))
finally:
    f.close()
for d in data_u:
    d.append("?")
f= open('data_s','rt')                                                      #opening the labelled data file

try:
    for line in f:
        line=line.rstrip('\n')
        data_s.append(line.split(','))
finally:
    f.close()
n=len(data_s)
k=input("enter value for k")  
while(len(data_u)!=0):                                                  #self training loop
    theta=logi(data_s)
#print theta
    temp=[]
    for i,d in enumerate(data_u):
        p=predict(d[0:len(d)-1],theta)
        temp.append(p)
        if p>=0.5:
            d[len(d)-1]="M"
        else:
            d[len(d)-1]="W"
    
    for i in range(len(temp)):
        temp[i]=float(abs(temp[i]-0.5)/0.5)                            #finding the confidence interval of each sample

    
    for i in range(k):
        for j,t in enumerate(temp):
            if t==max(temp) and t!=-1:
                data_s.append(data_u[j])                                #moving top k data points to labelled data set
                temp[j]=-1
                break
    dtemp=[]
    for i,d in enumerate(data_u):
        if temp[i]!=-1:
            dtemp.append(d)
    data_u=dtemp
    
#prin(data_s)
theta=logi(data_s)
f= open('data_t','rt')                                                      #opening the test data file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
tdatanew=copy.deepcopy(tdata)
for i,d in enumerate(tdatanew):                                            # Doing prediction for test data
    p=predict(map(float,d[0:len(d)-1]),theta)
    if p>=0.5:
        d[len(d)-1]="M"
    else:
        d[len(d)-1]="W"
print "labelled test data after self training"
prin(tdatanew)
acc=0
for i in range(len(tdata)):
    if(tdata[i][3]==tdatanew[i][3]):
        acc=acc+1
print "self training accuracy: ",(acc*100)/len(tdata),"%"

theta= logi(data_s[:n])                                                     #learning logistic on labelled data
tdatanew=copy.deepcopy(tdata)
for i,d in enumerate(tdatanew):
    p=predict(map(float,d[0:len(d)-1]),theta)
    if p>=0.5:
        d[len(d)-1]="M"
    else:
        d[len(d)-1]="W"
print "labelled test data after doing logistic regression on labelled data alone "
prin(tdatanew)
acc=0
for i in range(len(tdata)):
    if(tdata[i][3]==tdatanew[i][3]):
        acc=acc+1
print "logistic accuracy: ",acc*100/len(tdata),"%"



            
        
    
