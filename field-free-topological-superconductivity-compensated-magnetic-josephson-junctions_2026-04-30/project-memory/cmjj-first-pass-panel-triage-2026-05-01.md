# CMJJ First-Pass Panel Triage

## Scope
- Review target: the first executable CMJJ source-data bundle in `data/cmjj-source-data-2026-05-01/`
- Review date: 2026-05-01
- Review goal: decide which Figures 2-5 panels are already manuscript-facing candidates and which are still internal scaffolding

## Top-level verdict
The first-pass bundle is real progress and not a toy placeholder. It already contains enough structure to support a disciplined manuscript-facing next round. But it is not yet a final figure set. The strongest panels are the bulk-and-boundary layers in Figures 2 and 3. The weakest layer is the transport/false-positive discrimination logic in Figures 4 and 5, where the current observables are usable as execution baselines but not yet selective enough for a high-confidence venue claim.

## Figure 2
### Judgment
Keep and refine.

### Why
- The bundle shows a broad nontrivial `nu_ring = -1` region: 1010 grid points versus 261 trivial points in the current `mu-phi` scan.
- The cleanest low-gap points cluster near `phi = pi`, which is exactly the intended phase-controlled topology story.
- The refined cut at `mu = 1.0` shows a mostly nontrivial branch with a small trivial window, which is enough to build a story around a phase-tuned transition.

### Main risk
- The gap minima and topology flips are not yet visually calibrated for the sharpest possible main-text panel.
- A few small-gap points still sit in the trivial sector, so the final figure needs careful wording: this is a first transition map, not yet a polished "one-line proof" panel.

### Verdict
- Candidate for main text after plotting and mild parameter retuning.

## Figure 3
### Judgment
Keep and refine.

### Why
- The positive-control branch shows a strong near-zero window with large edge weights, typically `0.80-0.93`, in the same phase region where `nu_ring = -1`.
- The spectral-isolation metric becomes very large inside that window, from roughly `10^3` up to `2.3 x 10^5`, which is exactly the sort of separation needed for a persuasive boundary-state panel.
- Outside the topological window, the edge weight collapses to about `0.10`, so the contrast is already usable.

### Main risk
- The topological window is almost too clean numerically; the final text must not overclaim that near-zero energy alone proves topology.
- The trivial mimic profile exists, but the figure will only become strong after it is plotted side-by-side with the topological profile and a short caption explicitly naming the ambiguity.

### Verdict
- Strongest current panel family.
- Very likely to survive into the manuscript with only moderate figure work.

## Figure 4
### Judgment
Useful internal evidence, not yet a main-text-ready negative-control figure.

### Why
- The dot control clearly produces near-zero mimics, with the minimum energy dropping to about `2.2 x 10^-4`, so Control A is working.
- The impurity control also produces low-energy mimics, reaching about `3.2 x 10^-3`, so Control B is not empty.
- The disorder ensemble is especially useful as a stress test: as disorder increases, the median minimum energy drops sharply, and a small nontrivial fraction appears at strong disorder.

### Main risk
- The dot control currently flips to `nu_ring = -1` over the best near-zero region, which weakens its value as a clean "trivial" false-positive control.
- The impurity control is better behaved topologically, but its edge weight is almost zero, so it may look too easy to dismiss unless paired carefully with transport or local-spectrum evidence.
- The disorder panel shows some topology leakage at high disorder, which is scientifically honest but rhetorically dangerous if not framed as a stress-test rather than a simple failure case.

### Verdict
- Do not promote to final main text yet.
- Recompute this figure after deciding whether the negative controls should be forced into a strictly trivial regime or deliberately presented as ambiguity-producing stress tests.

## Figure 5
### Judgment
Execution success, manuscript risk still high.

### Why
- The transport package is real and phase-resolved, not a placeholder.
- The positive-control heatmap shows large nonlocal structure, with `|G_LR|` reaching about `0.78` in the current proxy.
- The dot and impurity controls also show sizable structure, so the transport layer is at least dynamic enough to be worth keeping.

### Main risk
- The current proxy is not yet selective enough. The positive case is stronger, but the dot and impurity controls are not suppressed nearly enough to make the diagnostic feel decisive.
- At zero bias, the dot mimic is already much smaller than the positive branch, which is good, but the impurity control still leaks enough structure that the final criterion will need tighter definition than raw `G_LR` magnitude.
- The disorder robustness scan shows the positive branch decays steadily toward zero with disorder; that is useful scientifically, but it means the present transport panel does not yet deliver a clean, broad robustness window.

### Verdict
- Keep as a reproducible baseline, not as a finished main-text panel.
- The next round should decide whether to keep the current wide-band proxy, switch to a stronger transport definition, or move the decisive claim toward a joint transport-plus-topology consistency panel.

## Ranking by current strength
1. Figure 3: best current panel family
2. Figure 2: good and likely salvageable for main text
3. Figure 4: scientifically useful but rhetorically unstable
4. Figure 5: real data, but current criterion still too weak for final claim load

## Recommended next action
Do not redraw everything at once. First retune the negative-control and transport layer around one concrete question:

Can the dot and impurity mimics be pushed into a regime where they still show misleading local near-zero structure but fail the final topology-and-transport consistency test more cleanly than they do now?

Until that is answered, Figures 2 and 3 can already be treated as near-main-text assets, while Figures 4 and 5 should remain marked as first-pass evidence.
