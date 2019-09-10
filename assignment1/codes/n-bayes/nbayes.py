import math as m


def norm(x, mean, var):                                      #function to find the normal distribution given the mean and variance
    denom = (2*m.pi*var)**.5
    num = m.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def prob(x,c,data):                                         #function to calculate probabilty.
    '''phe=0
    pwe=0
    pag=0'''
    pct=0
    temp=[0]*len(x)
    for d in data:                                #calculating the means for each attribute
        if d[len(x)].upper()==c.upper():
            pct=pct+1
            for i in range(len(x)):
                temp[i]=temp[i]+int(d[i])
    #print phe,pwe,pag
    pc=(float(pct))/(len(data))                 #probability of a given class
    mean=[0]*len(x)
    for i in range(len(x)):
        mean[i]=float(temp[i])/pct
    #print pc,mean    
    
    tempv=[0]*len(x)    
    for d in data:                              #calculating the variaces of each attribute
        if d[len(x)].upper()==c.upper():
            for i in range(len(x)):
                tempv[i]=tempv[i]+m.pow((float(d[i]))-mean[i],2)
    var=[0]*len(x)
    for i in range(len(x)):
        var[i]=float(tempv[i])/(pct-1)
    t=1
    for i in range(len(x)):
        t=t*norm(x[i],mean[i],var[i])
        
    
    print var
    return (pc*t)    #returning P(c)*(p(xi/c) for all i)
    
            
        
            
    


tdata=[]
f= open('data_a','rt')                  #reading the file and storing the training data in tdata
try:    
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()
print tdata
inp=raw_input("input the data in one of the formats ('h' , 'h,w,a' , 'h,w'...etc)\n")
inp=inp.split(',')


w=prob(inp,"W",tdata)
m=prob(inp,"M",tdata)
print "probability of W =",w                                #calculating for class W
print "probability of  M =",m                               #calculating for class M
if max(w,m)==w:
    print "class is 'W'"
elif max(w,m)==m:
    print "class is 'M'"
else:
    print("both classes are equally likely")
