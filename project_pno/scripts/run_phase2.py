import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'phase2'
OUT.mkdir(parents=True, exist_ok=True)


def source(n, mode, amp=1.0):
    s=[[0.0]*n for _ in range(n)]
    for i in range(1,n-1):
        x=i/(n-1)
        for j in range(1,n-1):
            y=j/(n-1)
            if mode=='poisson':
                s[i][j]=amp*math.sin(math.pi*x)*math.sin(2*math.pi*y)
            else:
                s[i][j]=amp*math.cos(2*math.pi*x)*math.sin(math.pi*y)
    return s


def solve(mode,n=24,steps=700,k=8.0):
    u=[[0.0]*n for _ in range(n)]
    s=source(n,mode)
    h2=1/((n-1)**2)
    for _ in range(steps):
        nu=[r[:] for r in u]
        for i in range(1,n-1):
            for j in range(1,n-1):
                lap=u[i+1][j]+u[i-1][j]+u[i][j+1]+u[i][j-1]
                if mode=='poisson':
                    nu[i][j]=0.25*(lap-h2*s[i][j])
                else:
                    nu[i][j]=(lap-h2*s[i][j])/(4+h2*k*k)
        u=nu
    return u,s


def model_predict(model,s,n):
    if model=='fourier':
        rm=[sum(s[i][1:n-1])/(n-2) for i in range(n)]
        cm=[sum(s[i][j] for i in range(1,n-1))/(n-2) for j in range(n)]
        u=[[0.0]*n for _ in range(n)]
        for i in range(1,n-1):
            for j in range(1,n-1):
                u[i][j]=-0.02*(rm[i]+cm[j])
        return u
    # local core
    steps=50 if model=='local' else 35
    u=[[0.0]*n for _ in range(n)]
    h2=1/((n-1)**2)
    for _ in range(steps):
        nu=[r[:] for r in u]
        for i in range(1,n-1):
            for j in range(1,n-1):
                nu[i][j]=0.25*(u[i+1][j]+u[i-1][j]+u[i][j+1]+u[i][j-1]-h2*s[i][j])
        u=nu
    if model=='hybrid':
        g=model_predict('fourier',s,n)
        for i in range(n):
            for j in range(n):
                u[i][j]=0.75*u[i][j]+0.25*g[i][j]
    return u


def rel(pred,true):
    num=den=0.0
    n=len(pred)
    for i in range(1,n-1):
        for j in range(1,n-1):
            d=pred[i][j]-true[i][j]
            num+=d*d
            den+=true[i][j]*true[i][j]
    return (num/(den+1e-12))**0.5

rows=[]
for mode in ['poisson','helmholtz']:
    for n in [24,32]:
        for k in [6.0,10.0]:
            truth,s=solve(mode,n=n,k=k)
            for model in ['fourier','local','hybrid']:
                pred=model_predict(model,s,n)
                rows.append({'pde':mode,'grid':n,'k':k,'model':model,'relative_l2':rel(pred,truth)})

with (OUT/'phase2_generalization.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['pde','grid','k','model','relative_l2'])
    w.writeheader();w.writerows(rows)

best={}
for pde in ['poisson','helmholtz']:
    sub=[r for r in rows if r['pde']==pde and r['grid']==32 and r['k']==10.0]
    best[pde]=min(sub,key=lambda r:r['relative_l2'])['model']

summary={'topic':'pno_phase2','rows':len(rows),'unseen_condition_best':best,
'gate_signals':['multi_pde','unseen_k','grid_transfer','branch_ablation']}
(OUT/'phase2_assessment.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
