from io import StringIO
from pylint.lint import Run

print(Run(["form.py"], do_exit=False))


# results = Run(["form.py"], do_exit=False)
# pylint_output = StringIO()  # Custom open stream
# reporter = TextReporter(pylint_output)
# Run(["test_file.py"], reporter=reporter, do_exit=False)
# print(pylint_output.getvalue())  # Retrieve and print the text report
