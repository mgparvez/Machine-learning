import math as m

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
            grd[i][j]=(a/len(x))*grd[i][j]                          #gradient= xT*(H-Y)
    return(grd)
    
#----------------------------------------------------Training-----------------------------------------------------------------
itr=10000
alpha=0.01
tdata=[]

f= open('data','rt')                                                      #opening the data file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
x=[]
y=[]
for d in tdata:
    x.append(map(float,d[:(len(d)-1)]))                                  #Extracting features (h,w,a) from data and storing in x
    if d[len(d)-1]=='M':                                                #Assingning values to class (M=1,W=0)
        y.append([1])
    else:
        y.append([0])
#prin(x)
#prin(y)
theta=[[0 for i in range(1)] for j in range(len(x[0]))]
#prin(theta)
#-----------------------------------------------Stochastic Gradient descent-------------------------------------------------------
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

print "Theta:"
prin(theta)                                                             #Learned parameters

#--------------------------------------------------Prediction--------------------------------------------------------------------

inp=raw_input("enter height weight and age h,w,a\n")                    #Getting input from user for prediction
inp=inp.split(',')
inp=map(float,inp)
xin=[]
xin.append(inp)
prob=sig(mul(xin,theta))
print "The class is :"
if prob[0][0]>=0.5:
    print "M"
else:
    print "W"
    
