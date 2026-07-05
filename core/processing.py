import numpy as np

def mix_sho(S, H, O,
            r_s, r_h,
            g_h, g_o,
            b_o):

    R = r_s * S + r_h * H
    G = g_h * H + g_o * O
    B = b_o * O

    R = np.clip(R, 0, None)
    G = np.clip(G, 0, None)
    B = np.clip(B, 0, None)

    return R, G, B


def apply_palette(palette):
    if palette == "Hubble SHO":
        return 0.8,0.2, 0.7,0.3, 1.0

    elif palette == "HOO Boost":
        return 0.0,0.0, 0.3,0.7, 1.0

    elif palette == "HOO Natural":
        return 0.0,0.0, 0.6,0.4, 1.0

    elif palette == "Hα Rich":
        return 0.2,0.8, 0.8,0.2, 0.8

    elif palette == "OIII Rich":
        return 0.0,0.3, 0.2,0.8, 1.0

    elif palette == "Foraxx Pro":
        return 0.6,0.4, 0.4,0.6, 1.0

    elif palette == "Gold & Blue":
        return 1.0,0.0, 0.5,0.5, 1.0

    elif palette == "Teal & Orange":
        return 0.9,0.1, 0.3,0.7, 1.0

    return 0.8,0.2, 0.7,0.3, 1.0