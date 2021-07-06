import json
from color_generator.generate_class import BROWSERS_COLORS_PATH

# language=HTML
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Browsers theme color support</title>
  <style>
    :root {
        --color-real: rgba(48, 48, 48, 255);
        --color-need: white;
    }
    body {
      display: flex;
      flex-direction: column;
      margin: 0;
      padding: 0;
      width: 100vh;
      font-family: sans-serif;
    }
    h1 {
      display: block;
      text-align: center;
      margin: 1em;
      width: 100vw;
    }
    .section {
      display: block;
      font-family: sans-serif;
      padding: 20px;
      font-size: 30px;
      text-align: center;
      margin: 0;
      width: 100%;
      background: linear-gradient(to right, var(--color-real) 50%, var(--color-need) 50%);
    }
  </style>
</head>
<body>
<h1>Browsers theme color</h1>
%CONTENT%
</body>
</html>
"""

browsers_colors = json.load(open(BROWSERS_COLORS_PATH))

content = '\n'.join(
    f"<h2>Browser: {browser}</h2>\n" + '\n'.join((
        f"<h3>Mode: {mode}</h3>\n" + '\n'.join((
            '<h4 class="section" style="'
            f'--color-real: {value};'
            f'--color-need: {key};'
            f'">{key}</h4>'

            for key, value in colors.items()
        ))

        for mode, colors in modes.items()
    ))

    for browser, modes in browsers_colors.items()
)

with open('colors_res.html', 'w', encoding='utf-8') as res:
    res.write(
        TEMPLATE.replace('%CONTENT%', content)
    )
