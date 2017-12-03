.PHONY: test ut_test ac_test lint env upload clean

MAKEFLAGS += --silent

test: ut_test ac_test lint

ut_test:
	coverage run --branch --source=poker_stats -m unittest discover -v test/ut '*_test.py'
	coverage report --omit='*/__init__.py,*/__main__.py,*/api.py,*/config.py,*/report_printer.py'

ac_test:
	test/ac/ac_test.sh

lint:
	pylint --rcfile=.pylintrc poker_stats

env: python_env
	echo
	echo "Don't forget to 'source python_env/bin/activate' before starting the work"
	echo

python_env:
	virtualenv python_env
	echo '. ./python_env/bin/activate && pip install -r requirements.txt' | $(SHELL)

upload: clean test
	git push --force heroku develop:master
	./setup.py sdist bdist_wheel upload

clean:
	find -name '*.pyc' -exec rm -f {} \;
	-rm -rf dist build poker_stats.egg-info
