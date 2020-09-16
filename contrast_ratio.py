def contrast_ratio(colorA, colorB):
    L1 = relative_luminance(colorA)
    L2 = relative_luminance(colorB)
    if L2 > L1:
        temp = L1
        L1 = L2
        L2 = temp
    return (L1 + 0.05) / (L2 + 0.05)


def relative_luminance(color):
    r, g, b = color
    RsRGB = float(r) / 255
    GsRGB = float(g) / 255
    BsRGB = float(b) / 255
    R = _(RsRGB)
    G = _(GsRGB)
    B = _(BsRGB)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def _(value):
    return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4
