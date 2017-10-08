.PHONY: test ac_test

MAKEFLAGS += --silent

test: ut_test ac_test

ut_test:
	test/ut/handparser_test.py
	test/ut/report_test.py

ac_test:
	test/ac/ac_test.sh
