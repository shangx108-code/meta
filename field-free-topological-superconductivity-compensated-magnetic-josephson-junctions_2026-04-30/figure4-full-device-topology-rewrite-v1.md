# Figure 4 Full-Device Topology Rewrite v1

## Purpose
Provide directly insertable manuscript language for the Figure 4 Results chain while preserving one crucial boundary: this text defines the intended full-device-topology argument, but it does not certify that the argument is numerically complete until the shared rerun with `nu_ring` and `P_topo` exists.

## Intended insertion point
- Main text: Results section immediately after the local-failure figure and before the broader diagnostic-map summary
- Figure caption: Figure 4 topology/robustness sentence
- Internal writing rule: use this block to replace the clean-backbone wording, not to imply that the missing rerun has already been performed

## Main-text replacement paragraph
We therefore test the putative rescue layer on the same inhomogeneous device instances that generate the misleading low-bias local features. For each tuned operating point, the manuscript-facing comparison is defined by four matched quantities: the local low-bias conductance response, the nonlocal conductance amplitude, a reopened-gap proxy, and a full-device class-D topology label obtained from the Pfaffian parity switch between periodic and anti-periodic boundary conditions in the corresponding inhomogeneous BdG Hamiltonian. This comparison is designed to separate spatially extended near-zero structure from a genuinely topological operating window. In the intended full-device benchmark, smooth-dot and impurity-driven false positives may still show conspicuous local low-bias features, and disorder can also generate strong apparent zero-bias structure, yet these families should fail to maintain simultaneous consistency between nonlocal transport, gap reopening, and stable topological parity over the same perturbation window. By contrast, the positive-control nanowire is expected to retain that combined consistency over a finite robustness window. The resulting claim is therefore not that any single transport trace is decisive, but that the manuscript-level discriminator is the joint persistence of transport and topology in the same inhomogeneous system.

## Figure 4 caption replacement
Figure 4 compares matched operating points with misleading local low-bias behavior across the positive-control and false-positive families, and then asks which cases preserve nonlocal transport, reopened-gap behavior, and full-device topological consistency simultaneously. The topology label is defined from the full inhomogeneous device Hamiltonian through a real-space class-D Pfaffian parity switch, so the transport and topology panels probe the same physical landscape rather than a cleaned backbone model.

## Claim-discipline note
- Allowed now: describe the Figure 4 target logic as a consistency-filter test.
- Allowed now: state that the clean-backbone proxy is insufficient and has been superseded at the manuscript-planning level.
- Not allowed yet: claim that the full-device topology discriminator has already been numerically validated in the shared pipeline.
- Not allowed yet: describe Figure 4 as final, submission-grade, or topology-complete.

## Activation rule
This rewrite becomes validated manuscript text only after a rerun exists in which:
1. the same inhomogeneous Hamiltonian is used for transport and topology,
2. `nu_ring` is evaluated for positive, smooth-dot, impurity, and disorder families,
3. `P_topo` is reported from local perturbations around the selected operating points,
4. the updated figure panels and operating-point table are regenerated from those rerun outputs.
