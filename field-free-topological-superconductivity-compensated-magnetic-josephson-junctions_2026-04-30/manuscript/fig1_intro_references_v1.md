# Fig. 1 prompt, four-paragraph Introduction draft, and 35-reference seed list

Project: field-free topological superconductivity in compensated-magnetic Josephson junctions  
Started: 2026-04-30  
Version: v1 drafting package  
Scope: manuscript framing only. Fig. 1 is conceptual; all later figures must be data-derived.

---

## 1. Fig. 1 GPT-images-2.0 prompt

### Main prompt

Create a clean Nature Physics-style conceptual schematic for a theoretical condensed-matter physics paper. The figure should show a compensated-magnetic Josephson junction platform for field-free topological superconductivity. Use a horizontal planar Josephson junction geometry: two superconducting leads on the left and right with phases +phi/2 and -phi/2, separated by a central compensated magnetic weak link. The magnetic weak link should have two sublattices with opposite spin arrows, zero net magnetization, and momentum-dependent spin splitting illustrated by a small inset showing alternating red/blue spin-split bands in k-space. Do not draw a uniform ferromagnetic stray field. Add a phase-bias knob labelled phi that drives a transition from a trivial near-zero mimic to a topological purified end-mode pair. At the two ends of the weak link, draw localized Majorana-like end modes as soft glowing zero-energy markers only on the topological side. Include a diagnostic workflow strip underneath with five icons: bulk gap closing/reopening, Z2 invariant flip, open-boundary end localization, impurity/disorder negative control, and nonlocal EC/CAR response. Use minimal colors, high contrast, white background, thin vector-like lines, journal-quality labels, no photorealism, no 3D rendering.

### Required labels

- Compensated magnetic weak link
- Zero net magnetization
- Superconducting phase bias phi
- Bulk gap closing / reopening
- Z2 flip
- Trivial near-zero mimic
- Topological purified pair
- Nonlocal EC/CAR diagnostic

### Negative prompt / avoid

Avoid photorealistic laboratory equipment, microscope images, random noise texture, unlabelled decorative wave patterns, exaggerated glowing effects, ferromagnetic stray-field arrows, data heatmaps, numerical axes, or any element that could be mistaken for a measured data plot.

### Caption seed

Figure 1 | Concept and diagnostic workflow. A compensated magnetic Josephson junction combines zero-net-magnetization spin splitting with a superconducting phase bias. The phase bias drives a bulk gap closing and reopening accompanied by a Z2 invariant flip. Because trivial near-zero edge-like states can appear on the pre-transition side, the topological assignment is based on the combined evidence of bulk topology, spectral purification, end localization, negative controls, and nonlocal EC/CAR response rather than on local near-zero modes alone.

---

## 2. Four-paragraph Introduction draft

### Paragraph 1: broad motivation

Majorana zero modes in topological superconductors provide a route to non-Abelian quasiparticles and fault-tolerant quantum information processing. Semiconductor-superconductor hybrids and planar Josephson junctions have become leading engineered platforms because their superconducting phase, density, spin-orbit coupling, and boundary geometry can be tuned in situ. In these devices, a topological superconducting phase is usually accessed by combining proximity-induced pairing with spin splitting and spin-momentum locking. However, the magnetic-field requirement creates an immediate materials and device challenge: the same field that helps drive the topological phase can also introduce orbital depairing, vortex formation, soft gaps, and uncontrolled spatial inhomogeneity. A field-free or low-stray-field route to topological superconductivity is therefore not only conceptually attractive, but also central to building scalable and diagnostically clean Majorana devices.

### Paragraph 2: bottleneck and literature gap

The central experimental difficulty is that local zero-bias or near-zero-energy features are not unique to topological Majorana modes. Smooth confinement, quantum-dot states, disorder, local potential impurities, and ordinary Andreev bound states can all generate near-zero signatures that imitate several expected Majorana responses. Planar Josephson junctions add an important phase-control knob, but they do not by themselves remove this false-positive problem. Recent altermagnetic-Josephson-junction proposals further show that compensated magnetic order can provide strong spin splitting without a net ferromagnetic moment, suggesting a route around the orbital and stray-field limitations of conventional Zeeman or ferromagnetic approaches. Yet this also raises a sharper standard for theory: a convincing compensated-magnetic platform must not merely show near-zero modes, but must demonstrate that those modes follow a bulk topological transition and remain distinguishable from trivial mimics under controlled negative tests.

### Paragraph 3: our concept and mechanism

Here we propose a compensated-magnetic Josephson junction in which a momentum-dependent spin splitting, generated without net magnetization, cooperates with superconducting phase bias to drive a topological superconducting transition. The minimal model contains a superconducting weak link with opposite magnetic sublattices whose Brillouin-zone average magnetization vanishes while the band structure retains a finite spin splitting. Tuning the superconducting phase difference produces a bulk gap closing and reopening along a well-defined parameter cut, accompanied by a change of a one-dimensional Z2 invariant. Open-boundary calculations then reveal near-zero end-mode pairs on the same phase-selected branch. Crucially, the transition is not identified from zero energy alone. We explicitly track spectral isolation, end localization, and the evolution of the lowest subgap states across the phase-driven Z2 flip.

### Paragraph 4: main results and evidence chain

Our results establish a diagnostic chain for field-free topological superconductivity in compensated magnetic Josephson junctions. First, bulk phase diagrams identify a phase-controlled low-gap corridor and isolate the cuts where gap closing and Z2 inversion coincide. Second, open-boundary spectra show that near-zero end modes evolve continuously through the transition, with the post-flip branch becoming spectrally purified rather than simply appearing from zero. Third, local impurity and weak-disorder negative controls show that trivial near-zero edge-like states can be sharpened on the pre-transition side, but they fail to reproduce the combined signature of a nontrivial invariant, phase-driven gap reopening, strong spectral isolation, disorder persistence, and nonlocal electron-hole response. This combined protocol positions the compensated-magnetic Josephson junction not only as a field-free Majorana platform, but also as a testbed for separating topological end modes from experimentally plausible false positives.

---

## 3. Reference seed list: 35 grouped references

Status note: this is a DOI-bearing seed bibliography for manuscript drafting. Before final submission, export all entries from Crossref/APS/Nature/IOP/SciPost into BibTeX and compare titles, author lists, journal, volume, page/article number, year, and DOI exactly.

### A. Foundational Majorana and topological-superconductivity literature

1. Kitaev, A. Y. Unpaired Majorana fermions in quantum wires. Physics-Uspekhi 44, 131-136 (2001). DOI: 10.1070/1063-7869/44/10S/S29.
2. Read, N. & Green, D. Paired states of fermions in two dimensions with breaking of parity and time-reversal symmetries and the fractional quantum Hall effect. Physical Review B 61, 10267-10297 (2000). DOI: 10.1103/PhysRevB.61.10267.
3. Ivanov, D. A. Non-Abelian statistics of half-quantum vortices in p-wave superconductors. Physical Review Letters 86, 268-271 (2001). DOI: 10.1103/PhysRevLett.86.268.
4. Nayak, C., Simon, S. H., Stern, A., Freedman, M. & Das Sarma, S. Non-Abelian anyons and topological quantum computation. Reviews of Modern Physics 80, 1083-1159 (2008). DOI: 10.1103/RevModPhys.80.1083.
5. Alicea, J. New directions in the pursuit of Majorana fermions in solid state systems. Reports on Progress in Physics 75, 076501 (2012). DOI: 10.1088/0034-4885/75/7/076501.
6. Beenakker, C. W. J. Search for Majorana fermions in superconductors. Annual Review of Condensed Matter Physics 4, 113-136 (2013). DOI: 10.1146/annurev-conmatphys-030212-184337.
7. Elliott, S. R. & Franz, M. Colloquium: Majorana fermions in nuclear, particle, and solid-state physics. Reviews of Modern Physics 87, 137-163 (2015). DOI: 10.1103/RevModPhys.87.137.
8. Sato, M. & Ando, Y. Topological superconductors: a review. Reports on Progress in Physics 80, 076501 (2017). DOI: 10.1088/1361-6633/aa6ac7.

### B. Engineered semiconductor, nanowire, and Josephson-junction platforms

9. Sau, J. D., Lutchyn, R. M., Tewari, S. & Das Sarma, S. Generic new platform for topological quantum computation using semiconductor heterostructures. Physical Review Letters 104, 040502 (2010). DOI: 10.1103/PhysRevLett.104.040502.
10. Lutchyn, R. M., Sau, J. D. & Das Sarma, S. Majorana fermions and a topological phase transition in semiconductor-superconductor heterostructures. Physical Review Letters 105, 077001 (2010). DOI: 10.1103/PhysRevLett.105.077001.
11. Oreg, Y., Refael, G. & von Oppen, F. Helical liquids and Majorana bound states in quantum wires. Physical Review Letters 105, 177002 (2010). DOI: 10.1103/PhysRevLett.105.177002.
12. Mourik, V. et al. Signatures of Majorana fermions in hybrid superconductor-semiconductor nanowire devices. Science 336, 1003-1007 (2012). DOI: 10.1126/science.1222360.
13. Das, A. et al. Zero-bias peaks and splitting in an Al-InAs nanowire topological superconductor as a signature of Majorana fermions. Nature Physics 8, 887-895 (2012). DOI: 10.1038/nphys2479.
14. Deng, M. T. et al. Majorana bound state in a coupled quantum-dot hybrid-nanowire system. Science 354, 1557-1562 (2016). DOI: 10.1126/science.aaf3961.
15. Hell, M., Leijnse, M. & Flensberg, K. Two-dimensional platform for networks of Majorana bound states. Physical Review Letters 118, 107701 (2017). DOI: 10.1103/PhysRevLett.118.107701.
16. Pientka, F., Keselman, A., Berg, E., Yacoby, A., Stern, A. & Halperin, B. I. Topological superconductivity in a planar Josephson junction. Physical Review X 7, 021032 (2017). DOI: 10.1103/PhysRevX.7.021032.
17. Nichele, F. et al. Scaling of Majorana zero-bias conductance peaks. Physical Review Letters 119, 136803 (2017). DOI: 10.1103/PhysRevLett.119.136803.
18. Zhang, H. et al. Quantized Majorana conductance. Nature 556, 74-79 (2018). DOI: 10.1038/nature26142.
19. Fornieri, A. et al. Evidence of topological superconductivity in planar Josephson junctions. Nature 569, 89-92 (2019). DOI: 10.1038/s41586-019-1068-8.
20. Ren, H. et al. Topological superconductivity in a phase-controlled Josephson junction. Nature 569, 93-98 (2019). DOI: 10.1038/s41586-019-1148-9.

### C. Altermagnetism, compensated magnetism, and competing field-free Josephson platforms

21. Baltz, V. et al. Antiferromagnetic spintronics. Reviews of Modern Physics 90, 015005 (2018). DOI: 10.1103/RevModPhys.90.015005.
22. Smejkal, L., Sinova, J. & Jungwirth, T. Beyond conventional ferromagnetism and antiferromagnetism: a phase with nonrelativistic spin and crystal rotation symmetry. Physical Review X 12, 031042 (2022). DOI: 10.1103/PhysRevX.12.031042.
23. Smejkal, L., Sinova, J. & Jungwirth, T. Emerging research landscape of altermagnetism. Physical Review X 12, 040501 (2022). DOI: 10.1103/PhysRevX.12.040501.
24. Krempasky, J., Smejkal, L., D'Souza, S. W. et al. Altermagnetic lifting of Kramers spin degeneracy. Nature 626, 517-522 (2024). DOI: 10.1038/s41586-023-06907-7.
25. Song, C., Bai, H., Zhou, Z. et al. Altermagnets as a new class of functional materials. Nature Reviews Materials 10, 473-485 (2025). DOI: 10.1038/s41578-025-00779-1.
26. Yang, G. Z. X., Sun, Z.-T., Xie, Y.-M. et al. Topological altermagnetic Josephson junctions. npj Quantum Materials (2026). DOI: 10.1038/s41535-026-00874-8.

### D. Nonlocal response, crossed Andreev reflection, and transport diagnostics

27. Nilsson, J., Akhmerov, A. R. & Beenakker, C. W. J. Splitting of a Cooper pair by a pair of Majorana bound states. Physical Review Letters 101, 120403 (2008). DOI: 10.1103/PhysRevLett.101.120403.
28. Law, K. T., Lee, P. A. & Ng, T. K. Majorana fermion induced resonant Andreev reflection. Physical Review Letters 103, 237001 (2009). DOI: 10.1103/PhysRevLett.103.237001.
29. Flensberg, K. Tunneling characteristics of a chain of Majorana bound states. Physical Review B 82, 180516(R) (2010). DOI: 10.1103/PhysRevB.82.180516.
30. Wimmer, M., Akhmerov, A. R., Dahlhaus, J. P. & Beenakker, C. W. J. Quantum point contact as a probe of a topological superconductor. New Journal of Physics 13, 053016 (2011). DOI: 10.1088/1367-2630/13/5/053016.
31. Schindele, J., Baumgartner, A. & Schonenberger, C. Near-unity Cooper pair splitting efficiency. Physical Review Letters 109, 157002 (2012). DOI: 10.1103/PhysRevLett.109.157002.

### E. False positives, quasi-Majoranas, disorder, and negative-control literature

32. Kells, G., Meidan, D. & Brouwer, P. W. Near-zero-energy end states in topologically trivial spin-orbit coupled superconducting nanowires with a smooth confinement. Physical Review B 86, 100503(R) (2012). DOI: 10.1103/PhysRevB.86.100503.
33. Liu, C.-X., Sau, J. D., Stanescu, T. D. & Das Sarma, S. Andreev bound states versus Majorana bound states in quantum dot-nanowire-superconductor hybrid structures: trivial versus topological zero-bias conductance peaks. Physical Review B 96, 075161 (2017). DOI: 10.1103/PhysRevB.96.075161.
34. Vuik, A., Nijholt, B., Akhmerov, A. R. & Wimmer, M. Reproducing topological properties with quasi-Majorana states. SciPost Physics 7, 061 (2019). DOI: 10.21468/SciPostPhys.7.5.061.
35. Pan, H. & Das Sarma, S. Physical mechanisms for zero-bias conductance peaks in Majorana nanowires. Physical Review Research 2, 013377 (2020). DOI: 10.1103/PhysRevResearch.2.013377.

---

## 4. Immediate manuscript-use guidance

- Cite Refs. 1-8 in Introduction paragraph 1.
- Cite Refs. 9-20 around engineered nanowire and planar Josephson platforms.
- Cite Refs. 21-26 when introducing compensated magnetic order and the direct competing TAJJ work.
- Cite Refs. 27-31 in the nonlocal EC/CAR diagnostic section.
- Cite Refs. 32-35 whenever discussing trivial near-zero mimics and negative controls.

## 5. Claims that must be avoided or softened

Avoid: "Zero modes appear only in the topological phase."  
Use: "Near-zero edge-like states may occur on the trivial side; the post-transition branch is distinguished by the joint evidence of Z2 inversion, gap reopening, spectral isolation, disorder persistence, and nonlocal response."

Avoid: "This is the first altermagnetic Josephson Majorana proposal."  
Use: "Unlike recent altermagnetic-Josephson-junction proposals that establish field-free topology, this work focuses on a compensated-magnetic diagnostic pipeline that explicitly excludes trivial near-zero mimics."
