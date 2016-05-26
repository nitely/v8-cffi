clean:
	rm -fr dist/ doc/_build/
	rm -fr v8cffi/src/*.o *.egg-info *.so *.cpp
	find . -name '__pycache__' | xargs rm -rf

docs:
	cd docs && make clean && make html

build: clean
	python v8cffi/v8_build.py

test: build
	python runtests.py

sdist: test clean
	python setup.py sdist

release: test clean
	python setup.py sdist upload

.PHONY: clean docs build test sdist release
