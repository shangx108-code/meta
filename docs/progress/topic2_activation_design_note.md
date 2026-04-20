# Topic 2 Activation Co-design Note (Compact No-Torch Study)

- Sweep scope: 4 activation families × 3 compact parameter settings each.
- Metrics tracked: accuracy, gradient stability proxy, insertion loss, effective dynamic range, NFOM.

## Observed characteristics
- Best NFOM settings favored moderate insertion loss and stable gradient proxy.
- Very aggressive slope settings tended to reduce gradient stability and lower NFOM.
- Dynamic range helped only when not coupled with excessive insertion loss.

## Recommendation for deeper ONN-style stacks
Prefer activation regions with balanced slope and smoothness (not max slope), keeping insertion loss moderate to preserve end-to-end optical efficiency.
