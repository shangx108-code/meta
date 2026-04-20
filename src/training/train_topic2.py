from src.models.activations import microring_like, oe_hybrid_like, saturable_absorber, thermal_like

ACTS = {
    "saturable": saturable_absorber,
    "microring": microring_like,
    "thermal": thermal_like,
    "oe_hybrid": oe_hybrid_like,
}
