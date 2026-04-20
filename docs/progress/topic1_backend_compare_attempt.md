# Topic 1 backend=torch compare attempt

- Objective: run the same Topic 1 pilot config on `backend=surrogate` and `backend=torch`, then compare `ablation_pairwise.csv` and `paper_ablation.svg`.
- Executed comparison driver: `scripts/run_topic1_backend_compare.sh`.
- Environment check result: PyTorch unavailable (`ModuleNotFoundError`), so torch pilot could not run in this environment.

## Generated outputs

- `outputs/topic1/backend_compare/surrogate/ablation_pairwise.csv`
- `outputs/topic1/backend_compare/surrogate/paper_ablation.svg`
- `outputs/topic1/backend_compare/backend_comparison.csv`
- `outputs/topic1/backend_compare/comparison_summary.md`

## Notes

- The comparison table marks all rows as `torch_unavailable` in this environment.
- To complete the requested direct surrogate-vs-torch comparison, rerun the same script in a PyTorch-enabled runtime.
