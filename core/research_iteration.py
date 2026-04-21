"""Run phase2 simulations, assess status, and decide stop gate for LPR/AP-style draft readiness."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd):
    subprocess.run(cmd, shell=True, check=True, cwd=ROOT)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


# Step 1 execution
run('python3 project_pno/scripts/run_phase2.py')
run('python3 project_prc/scripts/run_phase2.py')
run('python3 project_meta_adapt/scripts/run_phase2.py')

# Step 2 assessment
pno = load(ROOT / 'project_pno/results/phase2/phase2_assessment.json')
prc = load(ROOT / 'project_prc/results/phase2/phase2_assessment.json')
meta = load(ROOT / 'project_meta_adapt/results/phase2/phase2_assessment.json')

# Step 3 gate decision (content-completeness gate for drafting, not acceptance guarantee)
gates = {
    'pno': set(pno.get('gate_signals', [])) >= {'multi_pde', 'unseen_k', 'grid_transfer', 'branch_ablation'},
    'prc': set(prc.get('gate_signals', [])) >= {'capacity_curve', 'crosstalk_scan', 'parallel_interference'},
    'meta': set(meta.get('gate_signals', [])) >= {'fraction_scan', 'severity_scan', 'strategy_pareto'},
}
all_pass = all(gates.values())

result = {
    'run_id': 'run_2026-04-21_phase2_003',
    'gates': gates,
    'all_pass': all_pass,
    'interpretation': 'Pass means simulation content checklist for LPR/AP-style draft is complete; not a claim of journal acceptance.'
}

out = ROOT / 'workspace/reports/phase2_gate_result.json'
out.write_text(json.dumps(result, indent=2), encoding='utf-8')
