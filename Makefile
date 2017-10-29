.PHONY: test ut_test ac_test lint

MAKEFLAGS += --silent

test: ut_test ac_test lint

ut_test:
	python2.7 -m unittest discover -v test/ut "*_test.py"

ac_test:
	test/ac/ac_test.sh

lint:
	pylint --rcfile=.pylintrc api.py poker_stats.py poker_stats
