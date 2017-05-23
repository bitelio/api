.PHONY: install test clean

install:
	if [ ! -d env ]; then virtualenv env; fi
	env/bin/pip install -r requirements.txt
	env/bin/pip install nose rednose
	env/bin/python setup.py develop

test:
	env/bin/nosetests --rednose

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
