import streamlit as st
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# Mini Pantone TPX dataset (sample)
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
    r = int(hex_code[0:
