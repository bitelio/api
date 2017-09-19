.PHONY: install test clean

install:
	if [ ! -d env ]; then python3 -m venv env; fi
	env/bin/python setup.py develop

run: install
	python3 -m api

test:
	python3 setup.py nosetests

clean:
	rm -r env
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
