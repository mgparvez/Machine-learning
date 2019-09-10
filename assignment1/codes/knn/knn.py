import math as m

def dist(x,y):                                                              #function to calculate cartesian distance
    t=0
    for i in range(len(x)):
        t=t+pow(x[i]-y[i],2)
    return(m.sqrt(t),x)





tdata=[]

f= open('data_a','rt')                                                      #opening the file

try:
    for line in f:
        line=line.rstrip('\n')
        tdata.append(line.split(','))
finally:
    f.close()

#print tdata
k=input("enter value for k")                                                         
inp=raw_input("input the data in one of the formats ('h' , 'h,w,a' , 'h,w'...etc)\n")
inp=inp.split(',')
inp=map(int,inp)
print inp
distances=[]
print len(inp)
for d in tdata:                                                                         #calculating the distances
    x=map(int,d[:(len(inp))])
    print x
    temp=[]
    temp.extend(dist(x,inp))
    temp.append(d[len(inp)])
    distances.append(temp)

distances=sorted(distances, key=lambda x:x[0])                                          #sorting the obtained distances
print "the ",k,"nearest neighbours are [ distance , data, class]\n"
print distances[:k]                                                      #printing the k nearest neighbours

count={"W":0,"M":0}                                                      # creating a dictionary to count the number of occurance of a class    

for i in distances[:k]:
    if i[2].upper()=='W':
        count["W"]=count["W"]+1
    else:
        count["M"]=count["M"]+1

opclass=[c for c,v in count.items() if v == max(count.values())]         #finding the mle of the class
print opclass
       


