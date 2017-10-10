.PHONY: test ut_test ac_test lint

MAKEFLAGS += --silent
SRC = poker_stats.py poker_stats/config.py poker_stats/entity.py poker_stats/handfilter.py poker_stats/report.py

test: ut_test ac_test lint

ut_test:
	test/ut/handparser_test.py
	test/ut/report_test.py

ac_test:
	test/ac/ac_test.sh

lint:
	-pylint --enable=all --disable=C,R --reports=no $(SRC) 2>/dev/null
