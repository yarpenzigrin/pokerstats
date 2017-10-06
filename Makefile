.PHONY: test ac_test

MAKEFLAGS += --silent

test: ac_test

ac_test:
	test/ac_test.sh
