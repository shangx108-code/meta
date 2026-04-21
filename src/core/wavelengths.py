def nm_to_m(values_nm):
    return [v * 1e-9 for v in values_nm]


def bandwidth_proxy(values_nm):
    return 0.0 if len(values_nm) <= 1 else float(max(values_nm) - min(values_nm))
