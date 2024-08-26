





header = """
    <html>
    <head></head>

      <style>
        #tooltip {
        background: cornsilk;
        border: 1px solid black;
        border-radius: 5px;
        padding: 5px;
        font-size: 12px;
     }
      </style>

      <script>
        function showTooltip(evt, text) {
          let tooltip = document.getElementById("tooltip");
          tooltip.innerHTML = text;
          tooltip.style.display = "block";
          tooltip.style.left = evt.pageX + 10 + \'px\';
          tooltip.style.top = evt.pageY + 10 + \'px\';
        }

        function hideTooltip() {
          var tooltip = document.getElementById("tooltip");
          tooltip.style.display = "none";
        }
      </script>
    </head>

    <body>
    <div id="tooltip" display="none" style="position: absolute; display: none;"></div>
    <svg viewBox="-20 -20 800 430" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <pattern id="dhatch" patternUnits="userSpaceOnUse" width="4" height="4">
            <path d="M-1,1 l2,-2
                M0,4 l4,-4
                M3,5 l2,-2"
            style="stroke:green; stroke-width:1" />
        </pattern>
        <symbol id="chevron" width="20" height="10">
          <polygon points="0 0, 18 0, 20 5, 18 10, 0 10, 2 5" />
        </symbol>
    <rect y="-20" width="800" height="40" fill="#0094CA"/>
    <rect y="380" width="800" height="5" fill="#0094CA"/>
    <line x1="450" y1="200" x2="700" y2="200" style="stroke:rgb(0,0,0);stroke-width:2" />
    <circle cx="400" cy="200" r="48" stroke-width="1" fill="white" />
    <circle cx="400" cy="200" r="45" stroke-width="1" fill="#0094CA" />
    <text x="385" y="205" fill="white">ESS</text>
"""

footer = """
        </svg></body></html>
"""
