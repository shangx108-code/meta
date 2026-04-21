import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOPICS={
 'pno': ROOT/'workspace/papers/pno/manuscript.md',
 'prc': ROOT/'workspace/papers/prc/manuscript.md',
 'meta': ROOT/'workspace/papers/meta/manuscript.md',
}

KEYS=[
 ('abstract','## Abstract',0.08),
 ('methods','## 2. Methods',0.08),
 ('results','## 3. Results',0.08),
 ('claim_boundary','Claim boundaries',0.07),
 ('reproducibility','Reproducibility',0.07),
 ('ablation','Ablation',0.08),
 ('limitations','Limitations',0.08),
 ('statistics','Statistical',0.08),
 ('reviewer_refinement','Reviewer-driven refinement',0.06),
 ('design_law','phase-diagram',0.06),
]

res={}
for t,p in TOPICS.items():
    txt=p.read_text(encoding='utf-8')
    score=0.25
    det={}
    for name,pat,w in KEYS:
        hit=pat.lower() in txt.lower()
        det[name]=hit
        if hit: score+=w
    score=max(0.0,min(score,0.92))
    res[t]={'accept_prob':round(score,3),'criteria':det}

out=ROOT/'workspace/reports/strict_review_probabilities.json'
out.write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2))
