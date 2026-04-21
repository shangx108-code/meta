# Topic 2 Activation Co-design Note (Compact No-Torch Study)

## Sweep scope
- 4 activation families × 3 settings each:
  - saturable absorber-like
  - microring-like
  - thermal-like
  - optoelectronic hybrid-like
- Metrics: accuracy, gradient stability proxy, insertion loss, effective dynamic range proxy, NFOM.

## Key observations from current ranking
- `thermal` settings dominated top NFOM ranks in this compact run.
- Best row was `thermal/setting_0` with high gradient stability and moderate insertion loss.
- Very aggressive slopes tended to reduce gradient-stability proxy and hurt NFOM despite dynamic-range gains.

## Practical guidance for deeper ONN-style models (pre-torch)
Favor activation settings with:
1. near-unity gradient proxy,
2. moderate insertion loss,
3. non-collapsed dynamic range,
rather than maximizing slope alone.
