import colorsys

# HEX → RGB (0–1)
def hex_to_rgb_float(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return r, g, b

# RGB → HEX
def rgb_float_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)

# Generate scale
def generate_scale(hex_color):
    r, g, b = hex_to_rgb_float(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    steps = {
        50: 0.95, 100: 0.85, 200: 0.75, 300: 0.65,
        400: 0.55, 500: l,
        600: 0.45, 700: 0.35, 800: 0.25, 900: 0.15
    }

    scale = {}
    for key, lightness in steps.items():
        new_rgb = colorsys.hls_to_rgb(h, lightness, s)
        scale[key] = rgb_float_to_hex(new_rgb)

    return scale

# Simple brightness
def get_brightness(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return 0.299*r + 0.587*g + 0.114*b

# Generate roles from primary
def generate_palette(primary):
    brightness = get_brightness(primary)

    # detect mode
    mode = "dark" if brightness < 128 else "light"

    # generate base scale
    scale = generate_scale(primary)

    if mode == "light":
        background = scale[50]
        text = scale[900]
    else:
        background = scale[900]
        text = scale[50]

    # simple accent (shift hue)
    r, g, b = hex_to_rgb_float(primary)
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    accent_hue = (h + 0.1) % 1.0
    accent_rgb = colorsys.hls_to_rgb(accent_hue, l, s)
    accent = rgb_float_to_hex(accent_rgb)

    return {
        "mode": mode,
        "primary": primary,
        "background": background,
        "text": text,
        "accent": accent,
        "scale": scale
    }