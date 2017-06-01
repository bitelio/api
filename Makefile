.PHONY: install test clean

install:
	if [ ! -d env ]; then virtualenv env; fi
	env/bin/pip install -r requirements.txt
	env/bin/python setup.py develop

test:
	env/bin/pip install nose rednose coverage
	env/bin/nosetests --rednose --with-coverage --cover-xml --cover-package server

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
