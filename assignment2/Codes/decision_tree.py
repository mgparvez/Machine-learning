import csv
import  math as m
import pprint
import copy
import sys
sys.setrecursionlimit(3000)


eps=7./3 - 4./3 -1
attr={'capshape':{'b':0, 'c':0, 'x':0, 'f':0, 'k':0, 's':0},'capsurface':{'f':0, 'g':0, 'y':0,'s':0},'capcolor':{'n':0, 'b':0, 'c':0, 'g':0, 'r':0,'p':0, 'u':0, 'e':0, 'w':0, 'y':0, 't':0,'f':0},'bruise':{'t':0,'f':0},'odor':{ 'a':0, 'l':0, 'c':0, 'y':0, 'f':0,'m':0, 'n':0, 'p':0,'s':0}}
    
col={'capshape':1,'capsurface':2,'capcolor':3,'bruise':4,'odor':5}
bl=['e','p']
    
train='MushroomTrain.csv'                                                   #train file
test='MushroomTest.csv'                                                     #test file
    
def read_file(filename):
    tdata=[]
    f= open(filename,'rU')                                                      #opening the file

    try:
        read=csv.reader(f, dialect=csv.excel_tab)
        for line in read:
            #line=line.rstrip('\n')
            tdata.append(line[0].split(','))
    finally:
        f.close() 
    return(tdata)
        
    
def entropy(tdata):                                                         #function to calculate entropy
    pe=pp=0.0
    #tdata=self.read_file()
    for d in tdata:
        if d[0]=='e':
            pe+=1
        else:
            pp+=1
        
    pp=pp/len(tdata)
    pe=pe/len(tdata)
    #print pe,pp
    E=0
    
    E +=-pe*m.log(pe)/m.log(2)
    E +=-pp*m.log(pp)/m.log(2)
    return(E)
    
def gain(a,data,attribute):                                                           #function to calculate gain
    j=col[a]
    E=0.0
    #print E
    for val in attribute[a]:
        e=0.0
        for c in bl:
            num=den=0.0
            for d in data:
                if d[j]==val:
                    den+=1
                    if d[0]==c:
                        num+=1
            fraction= num/(den+eps)
            e += -fraction*m.log(fraction+eps)/m.log(2)
            #print a,val,num,den,c,"\n"
        ftemp=den/len(data)
        E+=-ftemp*e
    return(abs(E))


def choose_node(data,attribute):                                                      #choosing the node with maximum gain
    gains={}
    for a in attribute:
        gains[a]=(entropy(data)-gain(a,data,attribute))
        maxv=max(gains.values())
        for k,v in gains.items():
            if v==maxv:
                maxk=k
    #print gains
    return maxk 
        
    return node

def split(a,v,data):                                                        
    i=col[a]
    sdata=[]
    for d in data:
        if (d[i]==v):
            sdata.append(d)
    return(sdata)

def chk(data):                                                                       #checking if it is a pure set                     
    p=e=0.0
    for d in data:
        if d[0]=='e':
            e+=1
        else:
            p+=1
    return(p*e)
    
def create_tree(data,attribute,tree=None):                                                #function to build the tree recursively
    node=choose_node(data,attribute)
    if tree is None:
        tree={}
        tree[node]={}
    attr=attribute[node]
    temp=copy.deepcopy(attribute)
    #print temp
    temp.pop(node)
    for v in attr:
        split_data=split(node,v,data)
        if (len(split_data)==0):
            tree[node][v]="No Data"            
        elif (chk(split_data)==0):
            tree[node][v]=split_data[0][0]
        elif(bool(temp)==False):
            p=e=0.0
            for d in data:
                if d[0]=='e':
                    e+=1
                else:
                    p+=1
            if(p>=e):
                tree[node][v]="p"
            else:
                tree[node][v]="e"                    
        else:
            tree[node][v]=create_tree(split_data,temp)
    return(tree)

def predict(data,tree):                                                     #function to predict data
    for nodes in tree:
        v=data[col[nodes]]
        tree=tree[nodes][v]
        p=0
        
        if type(tree) is dict:
            p=predict(data,tree)
        else:
            p=tree
            break;
    return(p)
        
 #------------------------------------------------------------------------------------------------------       
tdata=read_file(train)

tree=create_tree(tdata,attr)
print "The Tree is:\n"
pprint.pprint(tree)
testdata=read_file(test)
su=0.0
i=0
acct=[0]
for d in testdata:
    i+=1
    if(predict(d,tree) == d[0]):
        su+=1
    acct.append(acct[i-1]+su/i)
        
print "\nTest Accuracy:", su*100/len(testdata),"%"
#print acct
su=0.0
i=0
acc=[0]
for d in tdata:
    i+=1
    if(predict(d,tree) == d[0]):
        su+=1
    acc.append(acc[i-1]+su/i)
        #print predict(d,tree),"||",d
        
print "\nTraining Accuracy:", su*100/len(tdata),"%"
#print acc
