.PHONY: test ut_test ac_test lint

MAKEFLAGS += --silent

test: ut_test ac_test lint

ut_test:
	test/ut/handparser_test.py
	test/ut/report_test.py

ac_test:
	test/ac/ac_test.sh

lint:
	-pylint --rcfile=.pylintrc poker_stats.py poker_stats
