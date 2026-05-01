# Topology Layer Upgrade Spec

## Purpose
Replace the current clean-backbone topology proxy with a manuscript-defensible inhomogeneous topological discriminator for the full device. This is the single highest-priority manuscript-facing task because Figure 4 cannot support a Nature Physics-level claim while the topology layer ignores the same dot, impurity, or disorder landscape that generates the misleading local peak.

## What this round fixes
- Freezes one precise replacement target for the current topology label.
- Defines the minimum observable bundle that must appear together in the next Figure 4 rebuild.
- Provides directly reusable manuscript text and caption language that do not overclaim.
- Converts the current qualitative bottleneck into an auditable numerical completion rule.

## Required replacement discriminator
Use a full-device class-D real-space invariant rather than the present clean-backbone criterion.

### Recommended definition
For each inhomogeneous parameter set, build the same BdG Hamiltonian used for the transport calculation, including the dot, impurity, or disorder profile. Then evaluate a ring-based Majorana number from the antisymmetrized Majorana-basis Hamiltonian:

- `A_PBC`: antisymmetric Majorana matrix for the full inhomogeneous device with periodic boundary conditions.
- `A_APBC`: the same matrix with anti-periodic boundary conditions.
- `nu_ring = sgn[Pf(A_PBC) * Pf(A_APBC)]`.

Interpretation:
- `nu_ring = -1`: topological parity switch consistent with a Majorana-supporting phase.
- `nu_ring = +1`: topologically trivial under the same inhomogeneous landscape.

This is preferable to the clean-backbone criterion because it tests the actual device Hamiltonian rather than a cleaned version with the misleading inhomogeneity removed.

## Minimal numerical bundle for the next rebuild
The next manuscript-facing Figure 4 must evaluate the following quantities at the same operating points and under the same device profile:

1. local low-bias conductance amplitude or peak score
2. nonlocal conductance amplitude `|G_LR|`
3. reopened bulk-gap proxy or finite-size min-gap proxy with an explicit threshold
4. full-device topology label `nu_ring`
5. robustness probability `P_topo`

Recommended robustness definition:
- sample barrier, temperature, and disorder-strength perturbations around each operating point
- define `P_topo` as the fraction of samples satisfying both `nu_ring = -1` and reopened-gap threshold

The manuscript should then compare `P_topo` against the zero-bias-peak probability or local-peak score. The intended message is not that one scalar is universal, but that local peak prevalence and topological consistency decouple strongly in false-positive families.

## Completion rule for the next numerical round
The topology layer is considered materially upgraded only if all of the following are met:

1. the same inhomogeneous Hamiltonian is used for transport and topology
2. at least one smooth-dot false positive and one impurity false positive produce misleading local low-bias peaks while keeping `P_topo` well below the positive control
3. the disorder family no longer dominates the visual story so strongly that the dot and impurity controls become secondary
4. the main text can state one sentence distinguishing local anomaly from topological consistency without hedging around the topology implementation

If any one of these is missing, Figure 4 remains a working figure rather than a submission figure.

## Figure 4 rewrite target
Figure 4 should stop presenting a binary "nonlocal rescue" story and instead present a consistency-filter story:

- Panel A: positive control versus false positives at matched misleading local low-bias behavior
- Panel B: nonlocal signal comparison
- Panel C: reopened-gap or min-gap comparison
- Panel D: `nu_ring` and `P_topo` summary across the same operating points

The key visual claim should become:
"Large local low-bias features can persist across all families, but only the positive-control window sustains nonlocal transport together with a reopened gap and a stable full-device topological parity."

## Directly reusable manuscript text
### Main-text paragraph
To test whether the nonlocal signal truly tracks a topological regime rather than merely a spatially extended near-zero state, we evaluated the transport observables and the topology label on the same inhomogeneous device Hamiltonian. For each tuned operating point, we computed the local and nonlocal conductances, a reopened-gap proxy, and a real-space class-D ring invariant obtained from the Pfaffian parity switch between periodic and anti-periodic boundary conditions. The resulting comparison shows that misleading local low-bias peaks can be engineered in smooth-dot and impurity-driven false positives, and disorder can also generate strong apparent zero-bias structure, but these cases fail to maintain simultaneous consistency between nonlocal transport, gap reopening, and the full-device topological parity. In contrast, the positive-control nanowire retains that consistency over a finite robustness window, indicating that the decisive discriminator is not the local anomaly alone, and not even the nonlocal signal alone, but the joint persistence of transport and topology in the same inhomogeneous system.

### Figure-caption sentence
The topology label is evaluated from the full inhomogeneous device via a real-space class-D Pfaffian parity switch, rather than from a clean-backbone proxy, so the transport and topology panels test the same physical landscape.

## Immediate blocker
The current workspace for this scheduled run contains only the project memory files and does not include the benchmark scripts or stored output bundles referenced in the earlier notes. Therefore this round freezes the manuscript-defining topology upgrade specification, but does not rerun the numerics.

## Next executable action
Implement `nu_ring` in the shared three-terminal code path, rebuild the Figure 4 operating-point table, and regenerate the figure only after the topology and transport layers are computed on the same inhomogeneous device instances.
