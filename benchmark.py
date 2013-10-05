import time

import leafblade
import io

benchmarks = []
data = {
	"title": "Example",
	"charset": '&quot;"><script></script><"'
}

leafblade_template = leafblade.Template("""
doctype

html
	head
		meta charset: "#{data.charset}"

		title "#{data.title} · Test"

	body
		h1 "It works!"

		p "Hello, world."
""")

def test_leafblade():
	return leafblade_template.render(data)

benchmarks.append(("Leaf Blade", test_leafblade))

try:
	from wheezy.template.engine import Engine
	from wheezy.template.loader import DictLoader
	from wheezy.template.ext.core import CoreExtension
	from wheezy.html.utils import escape_html as wheezy_escape

	wheezy_engine = Engine(loader=DictLoader({"template": """
@require(title, charset)
<!DOCTYPE html>

<html>
	<head>
		<meta charset="@charset!h">

		<title>@title!h · Test</title>
	</head>
	<body>
		<h1>It works!</h1>

		<p>Hello, world.</p>
	</body>
</html>
"""}), extensions=[CoreExtension()])
	wheezy_engine.global_vars.update({"h": wheezy_escape})
	wheezy_template = wheezy_engine.get_template("template")

	def test_wheezy():
		return wheezy_template.render(data)

	benchmarks.append(("Wheezy", test_wheezy))
except ImportError:
	pass

try:
	from jinja2 import Template

	jinja_template = Template("""
<!DOCTYPE html>

<html>
	<head>
		<meta charset="{{ charset|escape }}">

		<title>{{ title|escape }} · Test</title>
	</head>
	<body>
		<h1>It works!</h1>

		<p>Hello, world.</p>
	</body>
</html>
""")

	def test_jinja():
		return jinja_template.render(data)

	benchmarks.append(("Jinja2", test_jinja))
except ImportError:
	pass

def test_noop():
	pass

def test(name, callback):
	start = time.clock()
	iterations = 0

	while True:
		callback()
		iterations += 1

		end = time.clock()
		if end - start > 1:
			break

	print("{name:<20}{ops:>10,.0f} op/s".format(name=name, ops=iterations / (end - start)))
	print(callback())

for name, callback in benchmarks:
	test(name, callback)
