with open("templates/index.html", "r") as f:
    html = f.read()

debug_grid_code = """
<!-- Temporary Coordinate Grid Overlay for Layout Mapping -->
<div id="tempDebugGrid" style="position: fixed; inset: 0; z-index: 99999; pointer-events: none; display: grid; grid-template-columns: repeat(10, 1fr); grid-template-rows: repeat(10, 1fr); border: 2px solid rgba(244, 63, 94, 0.8);">
  <script>
    const gridContainer = document.getElementById('tempDebugGrid');
    for (let i = 1; i <= 100; i++) {
      const cell = document.createElement('div');
      cell.style.cssText = "border: 1px dashed rgba(94, 234, 212, 0.35); color: rgba(253, 224, 71, 0.85); font-size: 10px; font-weight: bold; padding: 4px;";
      cell.innerText = `Cell ${i}`;
      gridContainer.appendChild(cell);
    }
  </script>
</div>
</body>"""

if "</body>" in html and "tempDebugGrid" not in html:
    html = html.replace("</body>", debug_grid_code)
    with open("templates/index.html", "w") as f:
        f.write(html)
    print("DEBUG_GRID_ADDED_SUCCESS")
else:
    print("Grid already present or </body> not found.")
