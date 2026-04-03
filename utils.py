import colorsys

# -----------------------------
# BASIC CONVERSIONS
# -----------------------------

def hex_to_rgb_float(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return r, g, b

def rgb_float_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)

# -----------------------------
# SCALE GENERATION
# -----------------------------

def generate_scale(hex_color):
    r, g, b = hex_to_rgb_float(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    steps = {
        50: 0.95, 100: 0.85, 200: 0.75, 300: 0.65,
        400: 0.55, 500: l,
        600: 0.45, 700: 0.35, 800: 0.25, 900: 0.15, 950: 0.08
    }

    scale = {}
    for key, lightness in steps.items():
        new_rgb = colorsys.hls_to_rgb(h, lightness, s)
        scale[key] = rgb_float_to_hex(new_rgb)

    return scale

# -----------------------------
# BRIGHTNESS & CONTRAST
# -----------------------------

def get_brightness(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return 0.299*r + 0.587*g + 0.114*b

def luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255

    def adjust(c):
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4

    r, g, b = adjust(r), adjust(g), adjust(b)
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast_ratio(c1, c2):
    l1 = luminance(c1)
    l2 = luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def pick_text_color(background):
    black = "#000000"
    white = "#ffffff"
    
    if contrast_ratio(background, black) > contrast_ratio(background, white):
        return black
    else:
        return white

# -----------------------------
# COLOR ENHANCEMENTS
# -----------------------------

def soften_color(hex_color):
    r, g, b = hex_to_rgb_float(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    s = max(0.1, s * 0.3)
    return rgb_float_to_hex(colorsys.hls_to_rgb(h, l, s))

def generate_accents(primary):
    r, g, b = hex_to_rgb_float(primary)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    accents = []

    # Complementary
    comp_h = (h + 0.5) % 1.0
    accents.append(rgb_float_to_hex(colorsys.hls_to_rgb(comp_h, l, s)))

    # Analogous
    acc1 = (h + 0.08) % 1.0
    acc2 = (h - 0.08) % 1.0

    accents.append(rgb_float_to_hex(colorsys.hls_to_rgb(acc1, l, s)))
    accents.append(rgb_float_to_hex(colorsys.hls_to_rgb(acc2, l, s)))

    return accents

# -----------------------------
# ORIGINAL GENERATOR (KEEP)
# -----------------------------

def generate_palette(primary):
    brightness = get_brightness(primary)
    mode = "dark" if brightness < 128 else "light"

    scale = generate_scale(primary)

    if mode == "light":
        background = soften_color(scale[50])
    else:
        background = soften_color(scale[950])

    text = pick_text_color(background)
    accents = generate_accents(primary)

    return {
        "mode": mode,
        "primary": primary,
        "background": background,
        "text": text,
        "accents": accents,
        "scale": scale
    }

# -----------------------------
# NEW GENERATOR (V2)
# -----------------------------

def generate_palette_v2(primary, secondary=None, mode=None):
    # detect mode if not provided
    if mode is None:
        brightness = get_brightness(primary)
        mode = "dark" if brightness < 128 else "light"

    # primary scale
    primary_scale = generate_scale(primary)

    # secondary
    if secondary:
        secondary_scale = generate_scale(secondary)
    else:
        r, g, b = hex_to_rgb_float(primary)
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        sec_h = (h + 0.12) % 1.0
        sec_rgb = colorsys.hls_to_rgb(sec_h, l, s)
        secondary = rgb_float_to_hex(sec_rgb)
        secondary_scale = generate_scale(secondary)

    # background
    if mode == "light":
        background = soften_color(primary_scale[50])
    else:
        background = soften_color(primary_scale[950])

    # text
    text = pick_text_color(background)

    # accents + scales
    accents = generate_accents(primary)
    accent_scales = []

    for acc in accents:
        accent_scales.append({
            "base": acc,
            "scale": generate_scale(acc)
        })

    return {
        "mode": mode,
        "primary": {
            "base": primary,
            "scale": primary_scale
        },
        "secondary": {
            "base": secondary,
            "scale": secondary_scale
        },
        "background": background,
        "text": text,
        "accents": accent_scales
    }