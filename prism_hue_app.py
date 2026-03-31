import streamlit as st
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# Sample Pantone TPX colors
PANTONE_TPX = {
    "#F4C2C2": "Pantone 13-1520 TPX",
    "#FFDD00": "Pantone 13-0858 TPX",
    "#0077B6": "Pantone 19-4052 TPX",
    "#C4A484": "Pantone 16-1334 TPX",
    "#8A2BE2": "Pantone 18-3838 TPX",
    "#00FF7F": "Pantone 14-6316 TPX",
    "#FF4500": "Pantone 17-1564 TPX",
    "#6A5ACD": "Pantone 18-3830 TPX",
    "#FFD700": "Pantone 14-0957 TPX",
    "#40E0D0": "Pantone 15-5519 TPX"
}

def hex_to_cmyk(hex_code):
    hex_code = hex_code.lstrip('#')
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0

    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c*100), round(m*100), round(y*100), round(k*100)

def closest_pantone(hex_code):
    input_color = sRGBColor(
        int(hex_code[0:2],16),
        int(hex_code[2:4],16),
        int(hex_code[4:6],16),
        is_upscaled=True
    )
    input_lab = convert_color(input_color, LabColor)
    min_diff = float('inf')
    closest_name = ""
    for pantone_hex, pantone_name in PANTONE_TPX.items():
        pantone_color = sRGBColor(
            int(pantone_hex[1:3],16),
            int(pantone_hex[3:5],16),
            int(pantone_hex[5:7],16),
            is_upscaled=True
        )
        pantone_lab = convert_color(pantone_color, LabColor)
        diff = delta_e_cie2000(input_lab, pantone_lab)
        if diff < min_diff:
            min_diff = diff
            closest_name = pantone_name
    return closest_name

# Streamlit UI
st.set_page_config(page_title="PRISM + HUE", layout="centered")
st.title("🎨 PRISM + HUE")
st.write("Convert HEX colors to CMYK and find the closest Pantone TPX with a live preview.")

hex_input = st.text_input("Enter HEX code (e.g., #FF5733):", "#FF5733")

if st.button("Convert"):
    try:
        c, m, y, k = hex_to_cmyk(hex_input)
        pantone = closest_pantone(hex_input)
        st.success(f"**CMYK:** {c}%, {m}%, {y}%, {k}%")
        st.success(f"**Closest Pantone TPX:** {pantone}")
        st.markdown(
            f"<div style='width:100px; height:100px; background-color:{hex_input}; border:1px solid #000'></div>",
            unsafe_allow_html=True
        )
        st.code(f"HEX: {hex_input}\nCMYK: {c},{m},{y},{k}\nPantone: {pantone}", language="text")
    except Exception as e:
        st.error(f"Error: {e}")
