# Topic 4 Follow-up Note (Wavelength Multiplexing Only)

## Compact follow-up
- Ran crosstalk-weight sweep: `0.05`, `0.10`, `0.20`.
- Reported: task A accuracy, task B accuracy, mean crosstalk, throughput-efficiency.

## Interpretation
- Task metrics were stable across weights in this compact setting.
- Throughput-efficiency decreased as crosstalk penalty weight increased.
- Conclusion: wavelength multiplexing currently shows a **real but weak** tradeoff curve (proof of concept), not yet a strong multitask gain.

## Near-term recommendation
Keep wavelength mode only; improve synthetic task diversity before adding polarization/spatial branches.
