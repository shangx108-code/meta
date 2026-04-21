# Supplementary Information

## S1. Configuration Grid
- PNO: pde in {poisson, helmholtz}, grid in {24,32}, k in {6,10}, model in {fourier,local,hybrid}.
- PRC: crosstalk in {0,0.05,0.1,0.2,0.3}.
- META: severity in {0.4,0.7,1.0}, programmable fraction in {0.1,0.25,0.5}, strategy in {electronic,local,global}.

## S2. Metrics
- PNO: relative L2 against iterative PDE solver truth.
- PRC: memory capacity, NARMA10 NRMSE, classification error, interference composite.
- META: shifted accuracy, bounded recovery ratio, cost proxy, recovery-cost utility.

## S3. Failure Modes
- Fourier proxy underperforms on some Helmholtz settings.
- PRC shared-state coupling may distort task-specific readout.
- META local adaptation can degrade under high-severity shift.

## S4. Claim Boundaries
These results are simulation-only and are not hardware-validated.
