import csv, json, math, random
from pathlib import Path
random.seed(19)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'phase2'
OUT.mkdir(parents=True,exist_ok=True)
DIM=10
W=[random.uniform(-1,1) for _ in range(DIM)]


def make_data(n=500,severity=0.0):
    xs,ys=[],[]
    for i in range(n):
        y=1 if i%2==0 else 0
        mu=1.0 if y==1 else -1.0
        x=[random.gauss(mu,0.7) for _ in range(DIM)]
        if severity>0:
            # stronger non-stationary perturbation: attenuation + structured distortion + noise
            x=[(1-0.85*severity)*v + severity*0.8*math.sin(j+1) + random.gauss(0,0.25+0.35*severity) for j,v in enumerate(x)]
        xs.append(x);ys.append(y)
    return xs,ys

def score(x,g): return sum(g[i]*W[i]*x[i] for i in range(DIM))

def th_sign(xs,ys,g):
    s=[score(x,g) for x in xs]; pos=[s[i] for i in range(len(s)) if ys[i]==1]; neg=[s[i] for i in range(len(s)) if ys[i]==0]
    return ((sum(pos)/len(pos)+sum(neg)/len(neg))/2, 1 if sum(pos)>sum(neg) else -1)

def acc(xs,ys,g,t,sgn):
    ok=0
    for x,y in zip(xs,ys):
        p=1 if sgn*score(x,g)>t else 0
        ok+=1 if p==y else 0
    return ok/len(xs)

def tune(xs,ys,g,idx,steps=140,lr=0.03):
    q=g[:]
    for _ in range(steps):
        for i in idx:
            grad=0.0
            for x,y in zip(xs[:200],ys[:200]):
                z=score(x,q); p=1/(1+math.exp(-max(min(z,20),-20)))
                grad+=(p-y)*W[i]*x[i]
            q[i]-=lr*grad/200
    return q

def recovery(a_src,a_shift,a_new):
    gap=max(a_src-a_shift,0.02)
    val=(a_new-a_shift)/gap
    return max(min(val,1.5),-1.5)

src_x,src_y=make_data(severity=0.0)
base=[1.0]*DIM
ths,sgs=th_sign(src_x,src_y,base)
a_src=acc(src_x,src_y,base,ths,sgs)
rows=[]
for sev in [0.4,0.7,1.0]:
    sx,sy=make_data(severity=sev)
    a_shift=acc(sx,sy,base,ths,sgs)
    for frac in [0.1,0.25,0.5]:
        k=max(1,int(DIM*frac)); idx=sorted(range(DIM),key=lambda i:abs(W[i]),reverse=True)[:k]
        gl=tune(sx,sy,base,list(range(DIM)),steps=170)
        lc=tune(sx,sy,base,idx,steps=130)
        te,se=th_sign(sx[:200],sy[:200],base)
        tl,sl=th_sign(sx[:200],sy[:200],lc)
        tg,sg=th_sign(sx[:200],sy[:200],gl)
        a_e=acc(sx,sy,base,te,se); a_l=acc(sx,sy,lc,tl,sl); a_g=acc(sx,sy,gl,tg,sg)
        rows.extend([
            {'severity':sev,'fraction':frac,'strategy':'electronic','acc':a_e,'recovery':recovery(a_src,a_shift,a_e),'cost':0.2},
            {'severity':sev,'fraction':frac,'strategy':'local','acc':a_l,'recovery':recovery(a_src,a_shift,a_l),'cost':0.3+frac},
            {'severity':sev,'fraction':frac,'strategy':'global','acc':a_g,'recovery':recovery(a_src,a_shift,a_g),'cost':1.0},
        ])

with (OUT/'phase2_programmable_recovery.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['severity','fraction','strategy','acc','recovery','cost'])
    w.writeheader();w.writerows(rows)

best=max(rows,key=lambda r:r['recovery']-0.35*r['cost'])
summary={'topic':'meta_adapt_phase2','rows':len(rows),'source_accuracy':a_src,
'best_tradeoff':{k:best[k] for k in ['severity','fraction','strategy','recovery']},
'gate_signals':['fraction_scan','severity_scan','strategy_pareto','repeatable_recovery_metric']}
(OUT/'phase2_assessment.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
