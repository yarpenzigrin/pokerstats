.PHONY: test ut_test ac_test lint

MAKEFLAGS += --silent

test: ut_test ac_test lint

ut_test:
	coverage run --branch --source=poker_stats -m unittest discover -v test/ut '*_test.py'
	coverage report --omit='*/__init__.py,*/config.py,*/report_printer.py'

ac_test:
	test/ac/ac_test.sh

lint:
	pylint --rcfile=.pylintrc api.py poker_stats.py poker_stats
