import streamlit as st

# -----------------------------
# Base conversion functions
# -----------------------------

def hex_to_rgb(hex_code):
    hex_code = hex_code.strip().lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c*2 for c in hex_code])
    if len(hex_code) != 6:
        return None
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return r, g, b

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def rgb_to_cmyk(r, g, b):
    r_p, g_p, b_p = r/255, g/255, b/255
    k = 1 - max(r_p, g_p, b_p)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r_p - k) / (1 - k)
    m = (1 - g_p - k) / (1 - k)
    y = (1 - b_p - k) / (1 - k)
    return round(c*100), round(m*100), round(y*100), round(k*100)

def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = c/100, m/100, y/100, k/100
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b

# -----------------------------
# HSL helpers for tints/tones/shades
# -----------------------------

def rgb_to_hsl(r, g, b):
    r_p, g_p, b_p = r/255, g/255, b/255
    max_c = max(r_p, g_p, b_p)
    min_c = min(r_p, g_p, b_p)
    l = (max_c + min_c) / 2

    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        if max_c == r_p:
            h = (g_p - b_p) / d + (6 if g_p < b_p else 0)
        elif max_c == g_p:
            h = (b_p - r_p) / d + 2
        else:
            h = (r_p - g_p) / d + 4
        h /= 6
    return h, s, l

def hsl_to_rgb(h, s, l):
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        r = g = b = int(l * 255)
        return r, g, b

    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    r = hue_to_rgb(p, q, h + 1/3)
    g = hue_to_rgb(p, q, h)
    b = hue_to_rgb(p, q, h - 1/3)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

# -----------------------------
# Generate tints, shades, tones
# -----------------------------

def generate_tints_shades_tones(r, g, b, steps=10):
    h, s, l = rgb_to_hsl(r, g, b)

    tints = []
    shades = []
    tones = []

    for i in range(1, steps + 1):
        factor = i / (steps + 1)

        # Tints: increase lightness toward 1
        l_tint = l + (1 - l) * factor
        l_tint = min(1, max(0, l_tint))
        rt, gt, bt = hsl_to_rgb(h, s, l_tint)
        tints.append((rt, gt, bt))

        # Shades: decrease lightness toward 0
        l_shade = l * (1 - factor)
        l_shade = min(1, max(0, l_shade))
        rs, gs, bs = hsl_to_rgb(h, s, l_shade)
        shades.append((rs, gs, bs))

        # Tones: reduce saturation toward 0
        s_tone = s * (1 - factor)
        s_tone = min(1, max(0, s_tone))
        rto, gto, bto = hsl_to_rgb(h, s_tone, l)
        tones.append((rto, gto, bto))

    return tints, shades, tones

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="HEX ⇄ CMYK + Tints/Tones/Shades", page_icon="🎨")

st.title("🎨 HEX ⇄ CMYK Converter + Tints, Tones & Shades")
st.write("Convert between HEX and CMYK, and explore tints, tones, and shades of your color.")

# HEX → CMYK
st.subheader("HEX → CMYK")
hex_input = st.text_input("Enter HEX code", "#D4B39A")

rgb = None
if hex_input:
    rgb = hex_to_rgb(hex_input)
    if rgb:
        cmyk = rgb_to_cmyk(*rgb)
        st.write(f"**RGB:** {rgb}")
        st.write(f"**CMYK:** C {cmyk[0]}%, M {cmyk[1]}%, Y {cmyk[2]}%, K {cmyk[3]}%")
        st.color_picker("Preview", rgb_to_hex(*rgb), disabled=True)
    else:
        st.error("Invalid HEX format. Use something like #D4B39A.")

# CMYK → HEX
st.subheader("CMYK → HEX")
c = st.number_input("C (%)", 0, 100, 0)
m = st.number_input("M (%)", 0, 100, 0)
y = st.number_input("Y (%)", 0, 100, 0)
k = st.number_input("K (%)", 0, 100, 0)

if st.button("Convert CMYK → HEX"):
    rgb_from_cmyk = cmyk_to_rgb(c, m, y, k)
    hex_code = rgb_to_hex(*rgb_from_cmyk)
    st.write(f"**RGB:** {rgb_from_cmyk}")
    st.write(f"**HEX:** {hex_code}")
    st.color_picker("Preview (from CMYK)", hex_code, disabled=True)

# Tints, Tones, Shades (based on HEX input)
if rgb:
    st.subheader("Tints, Tones, and Shades")

    tints, shades, tones = generate_tints_shades_tones(*rgb, steps=8)

    def render_row(colors, label):
        st.markdown(f"**{label}**")
        cols = st.columns(len(colors))
        for col, (r, g, b) in zip(cols, colors):
            with col:
                hex_val = rgb_to_hex(r, g, b)
                cmyk_val = rgb_to_cmyk(r, g, b)
                st.markdown(
                    f"<div style='width:100%;height:40px;border-radius:6px;"
                    f"border:1px solid #ddd;background:{hex_val};'></div>",
                    unsafe_allow_html=True,
                )
                st.caption(f"{hex_val}\nC{cmyk_val[0]} M{cmyk_val[1]} Y{cmyk_val[2]} K{cmyk_val[3]}")

    render_row(tints, "Tints (lighter)")
    render_row(tones, "Tones (muted)")
    render_row(shades, "Shades (darker)")
