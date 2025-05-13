html = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Test</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <a href="/page">Link</a>
    <img src="/image.png">
  </body>
</html>"""

basepath = "/ssgen/"
html = html.replace('href="/', f'href="{basepath}')
html = html.replace('src="/', f'src="{basepath}')

print(html)
