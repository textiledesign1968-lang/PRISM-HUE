<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>HEX ⇄ CMYK Converter</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      padding: 40px;
      background: #f5f5f5;
      color: #222;
    }
    .card {
      max-width: 480px;
      margin: 0 auto;
      background: #fff;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    }
    h1 { font-size: 22px; margin-bottom: 16px; }
    label { font-size: 14px; font-weight: 600; display: block; margin-top: 16px; }
    input {
      width: 100%;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 14px;
      margin-top: 6px;
    }
    button {
      margin-top: 20px;
      padding: 10px 16px;
      border-radius: 8px;
      border: none;
      background: #222;
      color: #fff;
      font-size: 14px;
      cursor: pointer;
    }
    .preview {
      width: 100%;
      height: 60px;
      border-radius: 8px;
      border: 1px solid #ddd;
      margin: 16px 0;
    }
    .result { font-size: 14px; line-height: 1.6; }
  </style>
</head>
<body>
  <div class="card">
    <h1>HEX ⇄ CMYK Converter</h1>

    <label>HEX → CMYK</label>
    <input id="hexInput" placeholder="#D4B39A" />

    <label>CMYK → HEX (comma separated)</label>
    <input id="cmykInput" placeholder="0, 12, 22, 0" />

    <button onclick="convert()">Convert</button>

    <div id="preview" class="preview"></div>
    <div id="results" class="result"></div>
  </div>

  <script>
    function normalizeHex(hex) {
      hex = hex.trim();
      if (!hex.startsWith("#")) hex = "#" + hex;
      if (hex.length === 4) {
        const r = hex[1], g = hex[2], b = hex[3];
        hex = "#" + r + r + g + g + b + b;
      }
      return hex.toUpperCase();
    }

    function hexToRgb(hex) {
      hex = normalizeHex(hex);
      if (!/^#([0-9A-F]{6})$/.test(hex)) return null;
      return {
        r: parseInt(hex.slice(1, 3), 16),
        g: parseInt(hex.slice(3, 5), 16),
        b: parseInt(hex.slice(5, 7), 16),
        hex
      };
    }

    function rgbToCmyk(r, g, b) {
      const rp = r / 255, gp = g / 255, bp = b / 255;
      const k = 1 - Math.max(rp, gp, bp);
      if (k === 1) return { c: 0, m: 0, y: 0, k: 100 };
      const c = (1 - rp - k) / (1 - k);
      const m = (1 - gp - k) / (1 - k);
      const y = (1 - bp - k) / (1 - k);
      return {
        c: Math.round(c * 100),
        m: Math.round(m * 100),
        y: Math.round(y * 100),
        k: Math.round(k * 100)
      };
    }

    function cmykToRgb(c, m, y, k) {
      c /= 100; m /= 100; y /= 100; k /= 100;
      const r = 255 * (1 - c) * (1 - k);
      const g = 255 * (1 - m) * (1 - k);
      const b = 255 * (1 - y) * (1 - k);
      return {
        r: Math.round(r),
        g: Math.round(g),
        b: Math.round(b)
      };
    }

    function rgbToHex(r, g, b) {
      return (
        "#" +
        r.toString(16).padStart(2, "0") +
        g.toString(16).padStart(2, "0") +
        b.toString(16).padStart(2, "0")
      ).toUpperCase();
    }

    function convert() {
      const hexInput = document.getElementById("hexInput").value.trim();
      const cmykInput = document.getElementById("cmykInput").value.trim();
      const results = document.getElementById("results");
      const preview = document.getElementById("preview");

      let output = "";

      // HEX → CMYK
      if (hexInput) {
        const rgb = hexToRgb(hexInput);
        if (rgb) {
          const cmyk = rgbToCmyk(rgb.r, rgb.g, rgb.b);
          output += `<strong>HEX → CMYK</strong><br>
            HEX: ${rgb.hex}<br>
            CMYK: ${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%<br><br>`;
          preview.style.background = rgb.hex;
        } else {
          output += "Invalid HEX format.<br><br>";
        }
      }

      // CMYK → HEX
      if (cmykInput) {
        const parts = cmykInput.split(",").map(v => parseFloat(v.trim()));
        if (parts.length === 4 && parts.every(v => !isNaN(v))) {
          const rgb = cmykToRgb(parts[0], parts[1], parts[2], parts[3]);
          const hex = rgbToHex(rgb.r, rgb.g, rgb.b);
          output += `<strong>CMYK → HEX</strong><br>
            RGB: ${rgb.r}, ${rgb.g}, ${rgb.b}<br>
            HEX: ${hex}<br>`;
          preview.style.background = hex;
        } else {
          output += "Invalid CMYK format.";
        }
      }

      results.innerHTML = output;
    }
  </script>
</body>
</html>
