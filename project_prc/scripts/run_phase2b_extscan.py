import csv, math, random
from pathlib import Path
random.seed(17)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'phase2'
OUT.mkdir(parents=True,exist_ok=True)

def tanh(x):
    x=max(min(x,20),-20)
    ex=math.exp(x); enx=math.exp(-x)
    return (ex-enx)/(ex+enx)

def gen(T=1600): return [random.uniform(0,0.5) for _ in range(T)]
def narma10(u):
    y=[0.0]*len(u)
    for t in range(10,len(u)-1):
        y[t+1]=0.3*y[t]+0.05*y[t]*sum(y[t-i] for i in range(10))+1.5*u[t-9]*u[t]+0.1
    return y

def dclass(u,lag=6):
    y=[0]*len(u)
    for t in range(lag,len(u)): y[t]=1 if u[t-lag]>0.27 else 0
    return y

def run(u,g,c):
    x1=x2=0.0; s1=[]; s2=[]
    for t,v in enumerate(u):
        u2=u[t-1] if t>0 else 0.0
        n1=tanh(g*x1+0.8*v+c*x2); n2=tanh(g*x2+0.8*u2+c*x1)
        x1,x2=n1,n2; s1.append(x1); s2.append(x2)
    return s1,s2

def fit2(x,y):
    n=len(x);sx=sum(x);sx2=sum(v*v for v in x);sx3=sum(v**3 for v in x);sx4=sum(v**4 for v in x)
    sy=sum(y);sxy=sum(x[i]*y[i] for i in range(n));sx2y=sum((x[i]**2)*y[i] for i in range(n))
    A=[[n,sx,sx2],[sx,sx2,sx3],[sx2,sx3,sx4]];b=[sy,sxy,sx2y]
    for i in range(3):
        p=A[i][i] if abs(A[i][i])>1e-12 else 1e-12
        for j in range(i,3):A[i][j]/=p
        b[i]/=p
        for r in range(3):
            if r==i:continue
            f=A[r][i]
            for c in range(i,3):A[r][c]-=f*A[i][c]
            b[r]-=f*b[i]
    return b

def reg_err(s,y):
    sp=int(0.7*len(s));a,b,c=fit2(s[:sp],y[:sp]);p=[a+b*v+c*v*v for v in s[sp:]];t=y[sp:]
    mse=sum((p[i]-t[i])**2 for i in range(len(t)))/len(t);m=sum(t)/len(t);var=sum((v-m)**2 for v in t)/len(t)
    return (mse/(var+1e-12))**0.5

def cls_err(s,y):
    sp=int(0.7*len(s));thr=sum(s[:sp])/sp
    p=[1 if v>thr else 0 for v in s[sp:]];t=y[sp:]
    return 1-sum(1 for i in range(len(t)) if p[i]==t[i])/len(t)

u=gen();y1=narma10(u);y2=dclass(u)
rows=[]
for c in [i/100 for i in range(0,51,5)]:
    s1,s2=run(u,0.75,c)
    mix=[0.6*s1[i]+0.4*s2[i] for i in range(len(s1))]
    sn,sc=reg_err(s1,y1),cls_err(s2,y2)
    pn,pc=reg_err(mix,y1),cls_err(mix,y2)
    rows.append({'crosstalk':c,'interference':(pn-sn)+(pc-sc),'single_narma':sn,'parallel_narma':pn})

with (OUT/'phase2b_extscan.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
