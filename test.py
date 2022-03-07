from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter


f = open("pylinescore.txt", "w")
pylint_output = StringIO()  # Custom open stream
reporter = TextReporter(pylint_output)
Run(["blog.py"], reporter=reporter, do_exit=False)
f.write("---------------------------Blog.py---------------------------\n")
f.write(pylint_output.getvalue())
